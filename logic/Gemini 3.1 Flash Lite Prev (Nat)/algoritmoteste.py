O avaliador usa `put()` em vez de `set()`. Vou ajustar:
Os testes 9 e 10 falham porque meu código lança exceções para `max_size=0` e `ttl<=0`, mas o avaliador espera que o cache seja criado. Vou ajustar:
10/10 testes passaram. Vou limpar os caches:
Implementação concluída com sucesso. 10/10 testes passaram. O arquivo está em `testeopencode/algoritmoteste.py`.