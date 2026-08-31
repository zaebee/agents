import unittest
import os
import sys
import tempfile
import json
import pathlib
import shutil
from unittest.mock import patch, MagicMock

# This is a bit of a hack to make the imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from hive.components.scout_bee.source_file_transformer import SourceFileTransformer
from hive.components.scout_bee.repository_transformer import RepositoryTransformer
from hive.components.scout_bee.open_api_transformer import OpenApiTransformer
from hive.components.scout_bee.http_connector import HttpConnector
from hive.components.scout_bee.git_hub_connector import GitHubConnector
from hive.components.scout_bee.scout_session_aggregate import ScoutSessionAggregate
from hive.components.scout_bee.scout_api_command import ScoutApiCommand
from hive.components.scout_bee.scout_repository_command import ScoutRepositoryCommand

class TestTransformers(unittest.TestCase):
    """Consolidated tests for all transformer primitives."""

    def test_source_file_transformer(self):
        transformer = SourceFileTransformer()
        py_content = "class MyPyAggregate(Aggregate): pass"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as py_file:
            py_file.write(py_content)
            filepath = py_file.name

        try:
            components = transformer.execute(filepath)
            self.assertIn("MyPyAggregate", components["aggregates"])
        finally:
            os.remove(filepath)

    def test_repository_transformer(self):
        transformer = RepositoryTransformer()
        temp_dir = tempfile.mkdtemp()
        (pathlib.Path(temp_dir) / "test.py").touch()
        try:
            files = transformer.execute(temp_dir)
            self.assertEqual(len(files), 1)
            self.assertEqual(os.path.basename(files[0]), "test.py")
        finally:
            shutil.rmtree(temp_dir)

    def test_openapi_transformer(self):
        transformer = OpenApiTransformer()
        mock_spec = {"info": {"title": "Test API"}}
        raw_content = json.dumps(mock_spec).encode('utf-8')
        report = transformer.execute(raw_content)
        self.assertEqual(report["title"], "Test API")

class TestConnectors(unittest.TestCase):
    """Consolidated tests for all connector primitives."""

    @patch('requests.get')
    def test_http_connector(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'{"key": "value"}'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        connector = HttpConnector()
        content = connector.process("http://test.com")
        self.assertEqual(content, b'{"key": "value"}')

    @patch('git.Repo.clone_from')
    @patch('tempfile.mkdtemp', return_value="/fake/dir")
    def test_github_connector(self, mock_mkdtemp, mock_clone_from):
        connector = GitHubConnector()
        input_data = {"url": "https://a.com/b.git", "github_token": "token"}
        temp_dir = connector.process(input_data)
        mock_clone_from.assert_called_once_with("https://token@a.com/b.git", "/fake/dir")
        self.assertEqual(temp_dir, "/fake/dir")

class TestScoutSessionAggregate(unittest.TestCase):
    """Tests for the main aggregate orchestration."""

    def setUp(self):
        self.aggregate = ScoutSessionAggregate("test-session-123")

    @patch.object(HttpConnector, 'process', return_value=b'{"info": {"title": "Mock API"}}')
    @patch.object(OpenApiTransformer, 'execute', return_value={"title": "Mock API", "version": "1.0"})
    def test_handle_api_command(self, mock_execute, mock_process):
        """Tests the API scouting workflow."""
        command = ScoutApiCommand(url="http://mock.api")
        event = self.aggregate.handle(command)

        mock_process.assert_called_once_with("http://mock.api")
        mock_execute.assert_called_once_with(b'{"info": {"title": "Mock API"}}')

        self.assertEqual(event.aggregate_id, "test-session-123")
        self.assertEqual(event.report["title"], "Mock API")
        self.assertEqual(self.aggregate.status, "COMPLETED")

    @patch('shutil.rmtree')
    @patch.object(GitHubConnector, 'process', return_value="/fake/repo")
    @patch.object(RepositoryTransformer, 'execute', return_value=["/fake/repo/file.py"])
    @patch.object(SourceFileTransformer, 'execute', return_value={"aggregates": ["TestAgg"], "transformations": [], "connectors": []})
    def test_handle_repo_command(self, mock_source_execute, mock_repo_execute, mock_git_process, mock_rmtree):
        """Tests the repository scouting workflow."""
        command = ScoutRepositoryCommand(url="http://github.com/a/b.git")
        event = self.aggregate.handle(command)

        mock_git_process.assert_called_once()
        mock_repo_execute.assert_called_once_with("/fake/repo")
        mock_source_execute.assert_called_once_with("/fake/repo/file.py")

        self.assertEqual(event.report["repository"], "http://github.com/a/b.git")
        self.assertIn("TestAgg", event.report["components"]["aggregates"])
        self.assertEqual(self.aggregate.status, "COMPLETED")

if __name__ == '__main__':
    unittest.main()
