import threading
import time
from collections import OrderedDict
from typing import Any, Optional

class LRUCacheError(Exception):
    """Custom exception for invalid inputs."""
    pass

class LRUCacheTTL:
    def __init__(self, capacity: int, default_ttl: float):
        if not isinstance(capacity, int) or capacity <= 0:
            raise LRUCacheError("Capacity must be a positive integer.")
        if not isinstance(default_ttl, (int, float)) or default_ttl <= 0:
            raise LRUCacheError("TTL must be a positive number.")

        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            value, expiry = self.cache[key]
            if time.time() > expiry:
                del self.cache[key]
                return None
            
            # Move to end (LRU update)
            self.cache.move_to_end(key)
            return value

    def put(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        if ttl is not None and (not isinstance(ttl, (int, float)) or ttl <= 0):
            raise LRUCacheError("TTL must be a positive number.")
        
        expiry_duration = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + expiry_duration

        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            
            self.cache[key] = (value, expiry)
            
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)