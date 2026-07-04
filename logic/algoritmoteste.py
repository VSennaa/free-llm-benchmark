import threading
import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCacheTTLError(Exception):
    pass


class InvalidKeyTypeError(LRUCacheTTLError):
    pass


class InvalidValueType(LRUCacheTTLError):
    pass


class InvalidCapacityError(LRUCacheTTLError):
    pass


class InvalidTTLError(LRUCacheTTLError):
    pass


class LRUCacheTTL:
    def __init__(self, max_size: int, ttl: float):
        self._max_size = max_size
        self._ttl = ttl
        self._cache: OrderedDict[Any, tuple[Any, float]] = OrderedDict()
        self._lock = threading.RLock()

    def _is_key_valid(self, key: Any) -> bool:
        try:
            hash(key)
            return key is not None
        except TypeError:
            return False

    def _is_expired(self, timestamp: float) -> bool:
        if self._ttl <= 0:
            return True
        return time.time() - timestamp > self._ttl

    def _evict_expired(self) -> None:
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self._cache.items()
            if self._is_expired(timestamp)
        ]
        for key in expired_keys:
            del self._cache[key]

    def _evict_lru(self) -> None:
        if self._max_size > 0 and len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)

    def get(self, key: Any) -> Optional[Any]:
        if not self._is_key_valid(key):
            raise InvalidKeyTypeError("Key must be hashable and not None")
        
        with self._lock:
            self._evict_expired()
            
            if key not in self._cache:
                return None
            
            value, timestamp = self._cache[key]
            
            if self._is_expired(timestamp):
                del self._cache[key]
                return None
            
            del self._cache[key]
            self._cache[key] = (value, timestamp)
            return value

    def put(self, key: Any, value: Any) -> None:
        if not self._is_key_valid(key):
            raise InvalidKeyTypeError("Key must be hashable and not None")
        
        with self._lock:
            self._evict_expired()
            
            if key in self._cache:
                del self._cache[key]
            
            if self._max_size > 0 and self._ttl > 0:
                self._evict_lru()
                self._cache[key] = (value, time.time())

    def delete(self, key: Any) -> bool:
        if not self._is_key_valid(key):
            raise InvalidKeyTypeError("Key must be hashable and not None")
        
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def __getitem__(self, key: Any) -> Any:
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __delitem__(self, key: Any) -> None:
        if not self.delete(key):
            raise KeyError(key)

    def __len__(self) -> int:
        with self._lock:
            self._evict_expired()
            return len(self._cache)

    def __repr__(self) -> str:
        with self._lock:
            return f"LRUCacheTTL(max_size={self._max_size}, ttl={self._ttl}, items={len(self._cache)})"

    def keys(self):
        with self._lock:
            self._evict_expired()
            return list(self._cache.keys())

    def values(self):
        with self._lock:
            self._evict_expired()
            return [v for v, _ in self._cache.values()]

    def items(self):
        with self._lock:
            self._evict_expired()
            return [(k, v) for k, (v, _) in self._cache.items()]