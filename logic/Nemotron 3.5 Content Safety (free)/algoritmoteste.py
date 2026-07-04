Classe `LRUCacheTTL` implementada em `algoritmoteste.py` com:
- Thread-safety via `threading.RLock()`
- LRU eviction quando excede `max_size`
- TTL por chave (expira automaticamente)
- Exceções customizadas: `InvalidKeyTypeError`, `InvalidValueTypeError`, `InvalidTTLTypeError`
- Apenas biblioteca padrão (sem dependências externas)