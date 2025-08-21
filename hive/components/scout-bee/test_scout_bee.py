import unittest
import sys
import io
import os
import http.server
import socketserver
import threading
from unittest.mock import patch

# Add the component directory to the path to allow importing main
# This makes the test runnable from the root directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from main import scout_api

# --- Test HTTP Server to serve mock_openapi.json ---
PORT = 8088
# Get the directory of the current script to find mock_openapi.json
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Suppress logging to keep test output clean
        return

class TestScoutBee(unittest.TestCase):

    httpd = None
    server_thread = None

    @classmethod
    def setUpClass(cls):
        """Set up a simple HTTP server to serve the mock file."""
        # Use a reusable port to avoid issues in CI environments
        socketserver.TCPServer.allow_reuse_address = True
        cls.httpd = socketserver.TCPServer(("", PORT), Handler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """Shut down the HTTP server."""
        if cls.httpd:
            cls.httpd.shutdown()
            cls.httpd.server_close()
        if cls.server_thread:
            cls.server_thread.join()

    def test_scout_api_output(self):
        """Tests the output of the scout_api function against a mock OpenAPI spec."""
        mock_url = f"http://localhost:{PORT}/mock_openapi.json"

        # Redirect stdout to capture the print output
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            # We patch sys.exit to prevent the test from stopping
            with patch('sys.exit') as mock_exit:
                scout_api(mock_url)
        finally:
            sys.stdout = original_stdout # Restore stdout

        output = captured_output.getvalue()

        # Assertions to check if the output is correct
        self.assertIn("Scout Bee Report", output)
        self.assertIn("API Title: Mock API", output)
        self.assertIn("Version: 1.0.0", output)
        self.assertIn("Description: A mock API for testing the Scout Bee.", output)
        self.assertIn("Path: /test/endpoint", output)
        self.assertIn("Method: GET", output)
        self.assertIn("Summary: A test endpoint.", output)
        self.assertIn("[query] param1: A test parameter.", output)


if __name__ == '__main__':
    unittest.main()
