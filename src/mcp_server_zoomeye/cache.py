import time
from typing import Dict, Any, Optional

class ZoomeyeCache:
    """A simple cache implementation for ZoomEye API responses.
    
    This cache stores API responses with their expiration time to reduce
    the number of API calls and improve performance.
    """
    
    def __init__(self, ttl: int = 300):
        """Initialize the cache.
        
        Args:
            ttl (int, optional): Time to live in seconds. Defaults to 300 (5 minutes).
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a value from the cache.
        
        Args:
            key (str): The cache key.
            
        Returns:
            Optional[Dict[str, Any]]: The cached value or None if not found or expired.
        """
        if key not in self.cache:
            return None
        
        cache_entry = self.cache[key]
        if time.time() > cache_entry["expires_at"]:
            # Cache entry has expired
            del self.cache[key]
            return None
        
        return cache_entry["data"]
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """Set a value in the cache.
        
        Args:
            key (str): The cache key.
            value (Dict[str, Any]): The value to cache.
        """
        self.cache[key] = {
            "data": value,
            "expires_at": time.time() + self.ttl
        }
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def remove(self, key: str) -> None:
        """Remove a specific cache entry.
        
        Args:
            key (str): The cache key to remove.
        """
        if key in self.cache:
            del self.cache[key]
    
    def get_cache_key(self, qbase64: str, **kwargs) -> str:
        """Generate a cache key from the query parameters.
        
        Args:
            qbase64 (str): Base64 encoded query string.
            **kwargs: Additional query parameters.
            
        Returns:
            str: A unique cache key.
        """
        # Sort kwargs to ensure consistent key generation
        sorted_kwargs = sorted(kwargs.items())
        # Create a string representation of the parameters
        params_str = f"qbase64={qbase64}"
        for k, v in sorted_kwargs:
            if v is not None:
                params_str += f"&{k}={v}"
        
        return params_str