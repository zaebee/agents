import unittest
import os
import sys
import tempfile
import json
import pathlib
import shutil
from unittest.mock import patch, MagicMock

# This is a bit of a hack to make the imports work
# It ensures the project root is on the path to find dna_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from hive.components.scout_bee.source_file_transformer import SourceFileTransformer
from hive.components.scout_bee.repository_transformer import RepositoryTransformer
from hive.components.scout_bee.open_api_transformer import OpenApiTransformer
from hive.components.scout_bee.http_connector import HttpConnector
from hive.components.scout_bee.git_hub_connector import GitHubConnector
from hive.components.scout_bee.scout_session_aggregate import ScoutSessionAggregate
from hive.components.scout_bee.scout_api_command import ScoutApiCommand
from hive.components.scout_bee.scout_repository_command import ScoutRepositoryCommand

class TestSourceFileTransformer(unittest.TestCase):
    """
    Tests for the SourceFileTransformer.
    """

    def setUp(self):
        self.transformer = SourceFileTransformer()

    def test_analyze_ts_file(self):
        """Tests the TypeScript file analyzer logic within the transformer."""
        ts_content = """
        // A comment
        class MyCoolAggregate extends Aggregate { /* ... */ }
        class AnotherClass extends SomeOtherBase { /* ... */ }
        export class MyConnector extends Connector { /* ... */ }
        """
        # Create a temporary file to be analyzed
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as ts_file:
            ts_file.write(ts_content)
            filepath = ts_file.name

        try:
            components = self.transformer.transform(filepath)
            self.assertIn("MyCoolAggregate", components["aggregates"])
            self.assertIn("MyConnector", components["connectors"])
            self.assertEqual(len(components["transformations"]), 0)
            self.assertNotIn("AnotherClass", components["aggregates"] + components["connectors"] + components["transformations"])
        finally:
            os.remove(filepath)

    def test_analyze_py_file(self):
        """Tests the Python file analyzer logic within the transformer."""
        py_content = """
# A python comment
class MyPyAggregate(Aggregate):
    pass

class NotAComponent:
    pass

class MyPyTransformation(Transformation):
    pass
        """
        # Create a temporary file to be analyzed
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as py_file:
            py_file.write(py_content)
            filepath = py_file.name

        try:
            components = self.transformer.transform(filepath)
            self.assertIn("MyPyAggregate", components["aggregates"])
            self.assertIn("MyPyTransformation", components["transformations"])
            self.assertEqual(len(components["connectors"]), 0)
            self.assertNotIn("NotAComponent", components["aggregates"] + components["connectors"] + components["transformations"])
        finally:
            os.remove(filepath)

    def test_transform_unsupported_file(self):
        """Tests that an unsupported file type returns an empty result."""
        # Create a dummy file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as txt_file:
            txt_file.write("some text")
            filepath = txt_file.name

        try:
            components = self.transformer.transform(filepath)
            self.assertEqual(len(components["aggregates"]), 0)
            self.assertEqual(len(components["connectors"]), 0)
            self.assertEqual(len(components["transformations"]), 0)
        finally:
            os.remove(filepath)


class TestRepositoryTransformer(unittest.TestCase):
    """
    Tests for the RepositoryTransformer.
    """
    def setUp(self):
        self.transformer = RepositoryTransformer()
        self.temp_dir = tempfile.mkdtemp()

        # Create a dummy file structure
        (pathlib.Path(self.temp_dir) / "src").mkdir()
        (pathlib.Path(self.temp_dir) / "src" / "component1").mkdir()
        (pathlib.Path(self.temp_dir) / "src" / "component1" / "aggregate.py").touch()
        (pathlib.Path(self.temp_dir) / "src" / "component1" / "model.ts").touch()
        (pathlib.Path(self.temp_dir) / "README.md").touch()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_finds_source_files(self):
        """Tests that the transformer correctly finds .py and .ts files."""
        found_files = list(self.transformer.transform(self.temp_dir))
        self.assertEqual(len(found_files), 2)

        base_names = [os.path.basename(f) for f in found_files]
        self.assertIn("aggregate.py", base_names)
        self.assertIn("model.ts", base_names)

class TestOpenApiTransformer(unittest.TestCase):
    """
    Tests for the OpenApiTransformer.
    """
    def setUp(self):
        self.transformer = OpenApiTransformer()

    def test_parses_valid_spec(self):
        """Tests that a valid OpenAPI spec is parsed correctly."""
        mock_spec = {
            "info": {"title": "Test API", "version": "1.1"},
            "paths": {
                "/items": {
                    "get": {"summary": "Get items"}
                }
            }
        }
        raw_content = json.dumps(mock_spec).encode('utf-8')
        report = self.transformer.transform(raw_content)

        self.assertEqual(report["title"], "Test API")
        self.assertEqual(report["version"], "1.1")
        self.assertEqual(len(report["endpoints"]), 1)
        self.assertEqual(report["endpoints"][0]["path"], "/items")
        self.assertEqual(report["endpoints"][0]["method"], "GET")

    def test_handles_invalid_json(self):
        """Tests that invalid JSON returns a default report."""
        raw_content = b"{'not_json':}"
        report = self.transformer.transform(raw_content)
        self.assertEqual(report["title"], "N/A")
        self.assertEqual(len(report["endpoints"]), 0)


class TestHttpConnector(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_success(self, mock_get):
        """Tests a successful fetch from a URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"key": "value"}'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        connector = HttpConnector()
        content = connector.fetch("http://test.com")

        mock_get.assert_called_once_with("http://test.com")
        self.assertEqual(content, b'{"key": "value"}')


@patch('shutil.rmtree') # Mock rmtree to avoid file system side effects on failure
class TestGitHubConnector(unittest.TestCase):
    @patch('git.Repo.clone_from')
    @patch('tempfile.mkdtemp', return_value="/fake/temp/dir")
    def test_clone_success(self, mock_mkdtemp, mock_clone_from, mock_rmtree):
        """Tests a successful repository clone."""
        connector = GitHubConnector()
        temp_dir = connector.clone("http://github.com/test/repo.git")

        mock_mkdtemp.assert_called_once()
        mock_clone_from.assert_called_once_with("http://github.com/test/repo.git", "/fake/temp/dir")
        self.assertEqual(temp_dir, "/fake/temp/dir")


class TestScoutSessionAggregate(unittest.TestCase):
    def setUp(self):
        self.aggregate = ScoutSessionAggregate("test-session-123")

    @patch('shutil.rmtree')
    @patch.object(GitHubConnector, 'clone', return_value="/fake/dir")
    @patch.object(RepositoryTransformer, 'transform', return_value=["/fake/dir/file.py"])
    @patch.object(SourceFileTransformer, 'transform', return_value={"aggregates": ["TestAggregate"], "connectors": [], "transformations": []})
    def test_handle_scout_repo_command(self, mock_source_transformer, mock_repo_transformer, mock_clone, mock_rmtree):
        """Tests the full orchestration of scouting a repository."""
        command = ScoutRepositoryCommand(url="http://github.com/test/repo.git")
        self.aggregate.handle_command(command)

        mock_clone.assert_called_once_with("http://github.com/test/repo.git", None)
        mock_repo_transformer.assert_called_once_with("/fake/dir")
        mock_source_transformer.assert_called_once_with("/fake/dir/file.py")
        mock_rmtree.assert_called_once_with("/fake/dir") # Check that cleanup happens

        self.assertEqual(self.aggregate.status, "COMPLETED")
        self.assertIn("TestAggregate", self.aggregate.report["components"]["aggregates"])


    @patch.object(HttpConnector, 'fetch', return_value=b'{"info": {"title": "Mock"}}')
    @patch.object(OpenApiTransformer, 'transform', return_value={"title": "Mock", "version": "1.0", "description": "A mock API", "endpoints": []})
    def test_handle_scout_api_command(self, mock_transform, mock_fetch):
        """Tests the orchestration of scouting an API."""
        command = ScoutApiCommand(url="http://mock.api/spec.json")
        self.aggregate.handle_command(command)

        mock_fetch.assert_called_once_with("http://mock.api/spec.json")
        mock_transform.assert_called_once_with(b'{"info": {"title": "Mock"}}')
        self.assertEqual(self.aggregate.status, "COMPLETED")
        self.assertEqual(self.aggregate.report, {"title": "Mock", "version": "1.0", "description": "A mock API", "endpoints": []})


if __name__ == '__main__':
    unittest.main()
