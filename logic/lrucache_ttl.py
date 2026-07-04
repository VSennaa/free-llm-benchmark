import threading
import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCacheTTLTypeError(TypeError):
    """Exceção lançada quando tipos inválidos são passados."""
    pass


class LRUCacheTTL:
    def __init__(self, max_size: int, ttl: float):
        if not isinstance(max_size, int):
            raise LRUCacheTTLTypeError("max_size deve ser um inteiro")
        if not isinstance(ttl, (int, float)):
            raise LRUCacheTTLTypeError("ttl deve ser um número")
        if max_size <= 0:
            raise LRUCacheTTLTypeError("max_size deve ser maior que zero")
        if ttl <= 0:
            raise LRUCacheTTLTypeError("ttl deve ser maior que zero")
        
        self._max_size = max_size
        self._ttl = ttl
        self._cache: OrderedDict[Any, tuple[Any, float]] = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: Any) -> Optional[Any]:
        if not isinstance(key, (str, int, float, bool, tuple, bytes, type(None))):
            raise LRUCacheTTLTypeError("key deve ser um tipo hashable válido")
        
        with self._lock:
            if key not in self._cache:
                return None
            
            value, timestamp = self._cache[key]
            
            if time.time() - timestamp > self._ttl:
                del self._cache[key]
                return None
            
            self._cache.move_to_end(key)
            return value

    def put(self, key: Any, value: Any) -> None:
        if not isinstance(key, (str, int, float, bool, tuple, bytes, type(None))):
            raise LRUCacheTTLTypeError("key deve ser um tipo hashable válido")
        
        with self._lock:
            if key in self._cache:
                del self._cache[key]
            
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            
            self._cache[key] = (value, time.time())

    def delete(self, key: Any) -> bool:
        if not isinstance(key, (str, int, float, bool, tuple, bytes, type(None))):
            raise LRUCacheTTLTypeError("key deve ser um tipo hashable válido")
        
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

    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)

    def __repr__(self) -> str:
        with self._lock:
            items = ", ".join(f"{k}: {v[0]}" for k, v in self._cache.items())
            return f"LRUCacheTTL(max_size={self._max_size}, ttl={self._ttl}, items={{{items}}})"