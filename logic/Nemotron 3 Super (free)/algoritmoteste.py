import threading
import time
import collections


class InvalidKeyTypeError(TypeError):
    pass


class InvalidTTLError(ValueError):
    pass


class InvalidMaxSizeError(ValueError):
    pass


class LRUCacheTTL:
    def __init__(self, maxsize: int):
        if not isinstance(maxsize, int) or maxsize <= 0:
            raise InvalidMaxSizeError("maxsize must be a positive integer")
        self._maxsize = maxsize
        self._cache = collections.OrderedDict()
        self._lock = threading.RLock()

    def _validate_key(self, key):
        try:
            hash(key)
        except TypeError:
            raise InvalidKeyTypeError(f"Key {key!r} is not hashable")

    def _validate_ttl(self, ttl):
        if ttl is not None and not isinstance(ttl, (int, float)):
            raise InvalidTTLError("TTL must be a number or None")
        if ttl is not None and ttl < 0:
            raise InvalidTTLError("TTL cannot be negative")

    def set(self, key, value, ttl=None):
        self._validate_key(key)
        self._validate_ttl(ttl)
        with self._lock:
            if key in self._cache:
                del self._cache[key]
            if len(self._cache) >= self._maxsize:
                self._cache.popitem(last=False)
            expiry = None
            if ttl is not None:
                expiry = time.time() + ttl
            self._cache[key] = (value, expiry)
            self._cache.move_to_end(key)

    def get(self, key):
        self._validate_key(key)
        with self._lock:
            if key not in self._cache:
                raise KeyError(key)
            value, expiry = self._cache[key]
            now = time.time()
            if expiry is not None and now >= expiry:
                del self._cache[key]
                raise KeyError(key)
            self._cache.move_to_end(key)
            return value

    def __contains__(self, key):
        self._validate_key(key)
        with self._lock:
            if key not in self._cache:
                return False
            value, expiry = self._cache[key]
            now = time.time()
            if expiry is not None and now >= expiry:
                del self._cache[key]
                return False
            return True

    def __len__(self):
        with self._lock:
            return len(self._cache)