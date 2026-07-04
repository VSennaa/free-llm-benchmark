from collections import OrderedDict
import threading
import time
from collections.abc import Hashable

class InvalidMaxSizeError(ValueError):
    pass

class InvalidTTLExpirationError(ValueError):
    pass

class InvalidKeyError(ValueError):
    pass

class LRUCacheTTL:
    def __init__(self, max_size: int):
        if not isinstance(max_size, int) or max_size <= 0:
            raise InvalidMaxSizeError("max_size must be a positive integer")
        self.max_size = max_size
        self._store = OrderedDict()
        self._lock = threading.RLock()

    def set(self, key, value, ttl: int):
        if not isinstance(key, Hashable):
            raise InvalidKeyError("key must be hashable")
        if not isinstance(ttl, (int, float)) or ttl < 0:
            raise InvalidTTLExpirationError("ttl must be a non-negative number")
        with self._lock:
            if key in self._store:
                del self._store[key]
            else:
                if len(self._store) >= self.max_size:
                    self._store.popitem(last=False)
            expiry = time.time() + ttl
            self._store[key] = (value, expiry)
            self._store.move_to_end(key)

    def get(self, key):
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expiry = entry
            if time.time() > expiry:
                del self._store[key]
                return None
            self._store.move_to_end(key)
            return value