import threading
import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCacheTTLError(Exception):
    """Exceção base para erros do LRUCacheTTL."""
    pass


class InvalidKeyTypeError(LRUCacheTTLError):
    """Exceção para chaves de tipo inválido."""
    pass


class InvalidValueTypeError(LRUCacheTTLError):
    """Exceção para valores de tipo inválido."""
    pass


class InvalidCapacityTypeError(LRUCacheTTLError):
    """Exceção para capacidade de tipo inválido."""
    pass


class InvalidTTLTypeError(LRUCacheTTLError):
    """Exceção para TTL de tipo inválido."""
    pass


class LRUCacheTTL:
    def __init__(self, capacity: int, ttl: float):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise InvalidCapacityTypeError("capacity deve ser um inteiro")
        if not isinstance(ttl, (int, float)) or isinstance(ttl, bool):
            raise InvalidTTLTypeError("ttl deve ser um número")
        
        self._capacity = capacity
        self._ttl = ttl
        self._cache: OrderedDict[Any, tuple[Any, float]] = OrderedDict()
        self._lock = threading.Lock()
    
    def put(self, key: Any, value: Any) -> None:
        if key is None:
            raise InvalidKeyTypeError("key não pode ser None")
        if value is None:
            raise InvalidValueTypeError("value não pode ser None")
        
        with self._lock:
            if key in self._cache:
                del self._cache[key]
            
            if self._capacity > 0:
                if len(self._cache) >= self._capacity:
                    self._cache.popitem(last=False)
                
                expiry = time.time() + self._ttl
                self._cache[key] = (value, expiry)
    
    def get(self, key: Any) -> Optional[Any]:
        if key is None:
            raise InvalidKeyTypeError("key não pode ser None")
        
        with self._lock:
            if key not in self._cache:
                return None
            
            value, expiry = self._cache[key]
            
            if time.time() > expiry:
                del self._cache[key]
                return None
            
            del self._cache[key]
            self._cache[key] = (value, time.time() + self._ttl)
            return value
    
    def contains(self, key: Any) -> bool:
        if key is None:
            raise InvalidKeyTypeError("key não pode ser None")
        
        with self._lock:
            if key not in self._cache:
                return False
            
            value, expiry = self._cache[key]
            
            if time.time() > expiry:
                del self._cache[key]
                return False
            
            return True
    
    def remove(self, key: Any) -> bool:
        if key is None:
            raise InvalidKeyTypeError("key não pode ser None")
        
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def size(self) -> int:
        with self._lock:
            current_time = time.time()
            expired_keys = [k for k, (_, exp) in self._cache.items() if current_time > exp]
            for k in expired_keys:
                del self._cache[k]
            return len(self._cache)
    
    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
    
    def max_size(self) -> int:
        return self._capacity
    
    def ttl(self) -> float:
        return self._ttl