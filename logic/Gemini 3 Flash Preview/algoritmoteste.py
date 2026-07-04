import time
import threading
from collections import OrderedDict
from typing import Any, Optional

class LRUCacheTTLError(Exception):
    """Exceção base para LRUCacheTTL."""
    pass

class InvalidCapacityError(LRUCacheTTLError):
    """Lançada quando a capacidade não é um inteiro positivo."""
    pass

class InvalidTTLErr(LRUCacheTTLError):
    """Lançada quando o TTL não é um número positivo."""
    pass

class InvalidKeyError(LRUCacheTTLError):
    """Lançada quando a chave é inválida ou não é hashable."""
    pass

class LRUCacheTTL:
    def __init__(self, capacity: int, default_ttl: float):
        if not isinstance(capacity, int):
            raise InvalidCapacityError("A capacidade deve ser um número inteiro.")
        if capacity <= 0:
            raise InvalidCapacityError("A capacidade deve ser maior que zero.")
        if not isinstance(default_ttl, (int, float)):
            raise InvalidTTLErr("O TTL padrão deve ser um número (int ou float).")
        if default_ttl <= 0:
            raise InvalidTTLErr("O TTL padrão deve ser maior que zero.")
            
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: Any) -> Any:
        with self.lock:
            if key not in self.cache:
                return None
            
            value, expiry = self.cache[key]
            if time.time() > expiry:
                del self.cache[key]
                return None
            
            self.cache.move_to_end(key)
            return value

    def put(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        try:
            hash(key)
        except TypeError:
            raise InvalidKeyError(f"A chave do tipo {type(key)} não é hashable.")
            
        target_ttl = ttl if ttl is not None else self.default_ttl
        if not isinstance(target_ttl, (int, float)):
            raise InvalidTTLErr("O TTL deve ser um número (int ou float).")
        if target_ttl <= 0:
            raise InvalidTTLErr("O TTL deve ser maior que zero.")

        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            
            expiry = time.time() + target_ttl
            self.cache[key] = (value, expiry)
            
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    def __len__(self) -> int:
        with self.lock:
            now = time.time()
            expired_keys = [k for k, (v, e) in self.cache.items() if now > e]
            for k in expired_keys:
                del self.cache[k]
            return len(self.cache)