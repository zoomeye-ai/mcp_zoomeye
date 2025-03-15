import unittest
import time
from mcp_server_zoomeye.cache import ZoomeyeCache

class TestZoomeyeCache(unittest.TestCase):
    """Test cases for ZoomeyeCache class"""

    def setUp(self):
        """Set up test environment"""
        self.cache = ZoomeyeCache(ttl=1)  # 1 second TTL for testing
        self.test_key = "test_key"
        self.test_value = {"data": "test_value"}

    def test_set_and_get(self):
        """Test setting and getting a value from the cache"""
        self.cache.set(self.test_key, self.test_value)
        result = self.cache.get(self.test_key)
        self.assertEqual(result, self.test_value)

    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key from the cache"""
        result = self.cache.get("nonexistent_key")
        self.assertIsNone(result)

    def test_expiration(self):
        """Test cache entry expiration"""
        self.cache.set(self.test_key, self.test_value)
        # Wait for the cache entry to expire
        time.sleep(1.1)
        result = self.cache.get(self.test_key)
        self.assertIsNone(result)

    def test_remove(self):
        """Test removing a cache entry"""
        self.cache.set(self.test_key, self.test_value)
        self.cache.remove(self.test_key)
        result = self.cache.get(self.test_key)
        self.assertIsNone(result)

    def test_clear(self):
        """Test clearing all cache entries"""
        self.cache.set(self.test_key, self.test_value)
        self.cache.set("another_key", {"data": "another_value"})
        self.cache.clear()
        self.assertIsNone(self.cache.get(self.test_key))
        self.assertIsNone(self.cache.get("another_key"))

    def test_get_cache_key(self):
        """Test generating a cache key"""
        qbase64 = "dGVzdF9xdWVyeQ=="  # base64 encoded "test_query"
        key = self.cache.get_cache_key(
            qbase64=qbase64,
            page=1,
            pagesize=10,
            fields="ip,port"
        )
        expected_key = "qbase64=dGVzdF9xdWVyeQ==&fields=ip,port&page=1&pagesize=10"
        self.assertEqual(key, expected_key)

        # Test with None values
        key = self.cache.get_cache_key(
            qbase64=qbase64,
            page=1,
            pagesize=10,
            fields=None
        )
        expected_key = "qbase64=dGVzdF9xdWVyeQ==&page=1&pagesize=10"
        self.assertEqual(key, expected_key)

if __name__ == "__main__":
    unittest.main()