The file already exists with an implementation. Let me write my own implementation as requested:
The file `lrucache_ttl.py` has been created with a thread-safe LRU cache implementation with TTL support. It includes:

- **Custom exceptions**: `LRUCacheTTLError`, `InvalidKeyTypeError`, `InvalidValueTypeError`, `InvalidTTLTypeError`, `InvalidCapacityTypeError`
- **Thread-safe operations** using `RLock`
- **LRU eviction** when capacity is exceeded
- **TTL expiration** tracked per key
- **Methods**: `put`, `get`, `contains`, `remove`, `clear`, `size`
- **Properties**: `capacity`, `ttl`