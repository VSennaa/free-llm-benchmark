# CLAUDE.md - Diretrizes do Benchmark OpenCode
1. **RESTRIÇÃO SEVERA DE DISCO:** É estritamente PROIBIDO criar ambientes virtuais (`.venv`), instalar pacotes pesados ou gerar arquivos de log temporários gigantescos. Use APENAS a Standard Library do Python (3.10+).
2. **LIMPEZA IMEDIATA:** Todo script que rodar deve deletar pastas `__pycache__` e arquivos `.pyc` logo após a execução.
3. **ESTRUTURA DE PASTAS:**
   - `testeopencode/<nome-do-modelo>/algoritmoteste.py` (código gerado pelo modelo)
   - `testeopencode/avaliador.py` (script de teste e métricas)
   - `testeopencode/resultado.csv` (tabela final de resultados)
4. **IMPARCIALIDADE:** O avaliador deve rodar em sandbox local simples, capturando tempo de execução de CPU, pico de memória (usando `tracemalloc`) e taxa de acerto nos testes de unidade.
