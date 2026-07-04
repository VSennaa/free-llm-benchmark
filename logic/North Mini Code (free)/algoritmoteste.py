from collections import OrderedDict
import time
import threading
from typing import Optional, Any


class InvalidKeyTypeError(Exception):
    """Raised when a key is not a string."""


class InvalidValueTypeError(Exception):
    """Raised when a value is not a string."""


class InvalidTTLTypeError(Exception):
    """Raised when TTL is not an integer."""


class LRUCacheTTL:
    def __init__(self, max_size: int):
        if not isinstance(max_size, int):
            raise InvalidTypeError("max_size must be an integer")
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._cache = OrderedDict()
        self._ttl_data = {}
        self._max_size = max_size
        self._lock = threading.RLock()

    def get(self, key: str) -> Any:
        if not isinstance(key, str):
            raise InvalidKeyTypeError("Key must be a string")
        
        with self._lock:
            now = time.time()
            self._cleanup_expired(now)
            
            if key not in self._cache:
                return None
            
            self._cache.move_to_end(key)
            return self._cache[key]

    def set(self, key: str, value: Any, ttl: int) -> None:
        if not isinstance(key, str):
            raise InvalidKeyTypeError("Key must be a string")
        if not isinstance(value, str):
            raise InvalidValueTypeError("Value must be a string")
        if not isinstance(ttl, int):
            raise InvalidTTLTypeError("TTL must be an integer")
        if ttl < 0:
            raise ValueError("TTL must be non-negative")
        
        with self._lock:
            now = time.time()
            self._cleanup_expired(now)
            
            if key in self._cache:
                self._cache.pop(key)
            
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            
            self._cache[key] = value
            self._ttl_data[key] = now + ttl

    def _cleanup_expired(self, now: float) -> None:
        expired_keys = [
            key for key, expires_at in self._ttl_data.items()
            if expires_at <= now
        ]
        for key in expired_keys:
            self._cache.pop(key, None)
            self._ttl_data.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._ttl_data.clear()

    def _get_lru(self) -> list[str]:
        with self._lock:
            return list(self._cache.keys()) if self._cache else []