import threading
import time
from collections import OrderedDict

class InvalidKeyError(Exception):
    pass

class InvalidValueError(Exception):
    pass

class LRUCacheTTL:
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise InvalidValueError("max_size must be positive")
        self.max_size = max_size
        self._cache = OrderedDict()
        self._lock = threading.RLock()

    def _is_expired(self, expiry: float) -> bool:
        return time.time() >= expiry

    def get(self, key):
        with self._lock:
            if key not in self._cache:
                raise KeyError(key)
            value, expiry = self._cache[key]
            if self._is_expired(expiry):
                del self._cache[key]
                raise KeyError(key)
            self._cache.move_to_end(key)
            return value

    def put(self, key, value, ttl: int):
        if ttl < 0:
            raise InvalidValueError("ttl must be non-negative")
        try:
            hash(key)
        except TypeError:
            raise InvalidKeyError("key must be hashable")
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, time.time() + ttl)
            if len(self._cache) > self.max_size:
                self._cache.popitem(last=False)

    def __contains__(self, key):
        with self._lock:
            return key in self._cache

    def __len__(self):
        with self._lock:
            return len(self._cache)