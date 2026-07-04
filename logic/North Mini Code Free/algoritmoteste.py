The file exists but needs improvement. Let me write a complete implementation:
The test logic was incorrect. After `get('a')`, 'a' becomes MRU. Let me fix the test:
Let me clean up the implementation to match the exact requirements:
Let me write the final implementation matching the exact requirements:
Implementation complete. The file `lru_cache_ttl.py` contains the thread-safe `LRUCacheTTL` class with:
- LRU eviction via `OrderedDict`
- Per-key TTL in seconds
- Custom `InvalidKeyError` and `InvalidValueError` exceptions
- Thread safety via `RLock`
- Only standard library imports