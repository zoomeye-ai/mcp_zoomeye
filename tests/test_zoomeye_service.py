import os
import json
import base64
import unittest
import requests
from unittest.mock import patch, MagicMock

from mcp_server_zoomeye.server import ZoomeyeService, zoomeye_search


class TestZoomeyeService(unittest.TestCase):
    """Test cases for ZoomeyeService class"""

    def setUp(self):
        """Set up test environment"""
        # Set up test API key
        self.test_api_key = "test_api_key"
        os.environ["ZOOMEYE_API_KEY"] = self.test_api_key
        self.service = ZoomeyeService()

    def tearDown(self):
        """Clean up test environment"""
        # Remove test API key
        if "ZOOMEYE_API_KEY" in os.environ:
            del os.environ["ZOOMEYE_API_KEY"]

    def test_init_with_key_param(self):
        """Test initialization with key parameter"""
        service = ZoomeyeService(key="custom_key")
        self.assertEqual(service.key, "custom_key")

    def test_init_with_env_var(self):
        """Test initialization with environment variable"""
        self.assertEqual(self.service.key, self.test_api_key)

    def test_init_without_key(self):
        """Test initialization without key"""
        if "ZOOMEYE_API_KEY" in os.environ:
            del os.environ["ZOOMEYE_API_KEY"]
        service = ZoomeyeService()
        self.assertIsNone(service.key)

    @patch("requests.post")
    def test_query_success(self, mock_post):
        """Test successful query"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 60000, "message": "success", "data": []}
        mock_post.return_value = mock_response

        # Test query
        query = "app=\"Apache Tomcat\""
        qbase64 = base64.b64encode(query.encode()).decode()
        result = self.service.query(qbase64=qbase64)

        # Verify result
        self.assertEqual(result, {"code": 60000, "message": "success", "data": []})

        # Verify request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["headers"]["API-KEY"], self.test_api_key)
        self.assertEqual(kwargs["json"]["qbase64"], qbase64)

    @patch("requests.post")
    def test_query_with_optional_params(self, mock_post):
        """Test query with optional parameters"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 60000, "message": "success", "data": []}
        mock_post.return_value = mock_response

        # Test query with optional parameters
        query = "app=\"Apache Tomcat\""
        qbase64 = base64.b64encode(query.encode()).decode()
        result = self.service.query(
            qbase64=qbase64,
            page=2,
            pagesize=20,
            fields="ip,port",
            sub_type="v4",
            facets="country",
            ignore_cache=True
        )

        # Verify request
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["page"], 2)
        self.assertEqual(kwargs["json"]["pagesize"], 20)
        self.assertEqual(kwargs["json"]["fields"], "ip,port")
        self.assertEqual(kwargs["json"]["sub_type"], "v4")
        self.assertEqual(kwargs["json"]["facets"], "country")
        self.assertEqual(kwargs["json"]["ignore_cache"], True)

    @patch("requests.post")
    def test_query_http_error(self, mock_post):
        """Test query with HTTP error"""
        # Mock response
        mock_post.side_effect = requests.exceptions.RequestException("HTTP Error")

        # Test query
        query = "app=\"Apache Tomcat\""
        qbase64 = base64.b64encode(query.encode()).decode()

        # Verify exception
        with self.assertRaises(ValueError) as context:
            self.service.query(qbase64=qbase64)
        self.assertIn("Error querying ZoomEye API", str(context.exception))

    @patch("requests.post")
    def test_query_json_error(self, mock_post):
        """Test query with JSON error"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("JSON Error", "", 0)
        mock_post.return_value = mock_response

        # Test query
        query = "app=\"Apache Tomcat\""
        qbase64 = base64.b64encode(query.encode()).decode()

        # Verify exception
        with self.assertRaises(ValueError) as context:
            self.service.query(qbase64=qbase64)
        self.assertEqual("Invalid JSON response from ZoomEye API", str(context.exception))

    def test_query_no_api_key(self):
        """Test query without API key"""
        # Create service without API key
        if "ZOOMEYE_API_KEY" in os.environ:
            del os.environ["ZOOMEYE_API_KEY"]
        service = ZoomeyeService()

        # Test query
        query = "app=\"Apache Tomcat\""
        qbase64 = base64.b64encode(query.encode()).decode()

        # Verify exception
        with self.assertRaises(ValueError) as context:
            service.query(qbase64=qbase64)
        self.assertIn("ZoomEye API key is required", str(context.exception))


if __name__ == "__main__":
    unittest.main()