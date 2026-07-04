O avaliador usa `max_size` e métodos `put`/`get`. Vou ajustar a classe:
7/10 testes passaram. Vou verificar quais testes falharam:
O teste 9 falha porque max_size=0 não descarta corretamente. Vou ajustar:
8/10 testes passaram. Vou verificar os testes restantes:
O teste 2 falha. O problema é `move_to_end` em `put` quando a chave não existe:
O arquivo foi sobrescrito. Vou recriá-lo com a implementação correta:
9/10 testes passam. Vou verificar o teste restante:
Teste 4 passa. Vou verificar o teste 5:
Todos os testes passam individualmente. Vou rodar o avaliador novamente:
O arquivo foi sobrescrito. Vou recriá-lo corretamente:
O teste 9 falha. O problema é a lógica de max_size=0. Vou corrigir:
10/10 testes passam. Vou copiar o arquivo final:
10/10 testes passaram. Vou limpar os caches: