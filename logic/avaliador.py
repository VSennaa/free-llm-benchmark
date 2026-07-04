import os
import sys
import time
import tracemalloc
import importlib.util
import csv
import shutil
import threading

# Importar Modelos do runner
from benchmark_runner import MODELOS

def clean_cache(base_path):
    """Remove pastas __pycache__ e arquivos .pyc"""
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
        for f in files:
            if f.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, f))
                except OSError:
                    pass

def run_tests(module):
    """
    Roda 10 unit tests de alta rigorosidade na classe LRUCacheTTL.
    Retorna (testes_passados, total_testes)
    """
    total_tests = 10
    tests_passed = 0
    
    if not hasattr(module, 'LRUCacheTTL'):
        return 0, total_tests
        
    LRUCacheTTL = module.LRUCacheTTL
    
    # 1. Teste de inserção e busca básica
    def test_1_basic_put_get():
        cache = LRUCacheTTL(max_size=3, ttl=10)
        cache.put("a", 1)
        assert cache.get("a") == 1
        
    # 2. Teste de descarte por limite de tamanho (LRU)
    def test_2_lru_eviction():
        cache = LRUCacheTTL(max_size=2, ttl=10)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    # 3. Teste de expiração por TTL
    def test_3_ttl_expiration():
        cache = LRUCacheTTL(max_size=2, ttl=0.1)
        cache.put("a", 1)
        time.sleep(0.15)
        assert cache.get("a") is None

    # 4. Teste de atualização de ordem LRU no acesso e atualização
    def test_4_lru_update():
        cache = LRUCacheTTL(max_size=2, ttl=10)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a") # acessa "a", tornando "b" o menos recentemente usado
        cache.put("c", 3) # evicta "b"
        assert cache.get("b") is None
        assert cache.get("a") == 1

    # 5. Teste de validação de tipos nulos e exceções customizadas
    def test_5_invalid_types_exceptions():
        cache = LRUCacheTTL(max_size=2, ttl=10)
        try:
            cache.put(None, 1) # Chave inválida
            return False
        except Exception:
            pass
        return True

    # 6. Teste de concorrência básica (Thread-safety)
    def test_6_thread_safety():
        cache = LRUCacheTTL(max_size=100, ttl=10)
        def worker(i):
            cache.put(f"k{i}", i)
            cache.get(f"k{i}")
            
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        # O cache não deve quebrar ou corromper (apenas verifica integridade básica)
        assert cache.get("k0") == 0 or cache.get("k0") is None
        
    # 7. Teste de chave string vazia
    def test_7_empty_key():
        cache = LRUCacheTTL(max_size=2, ttl=10)
        cache.put("", "vazio")
        assert cache.get("") == "vazio"

    # 8. Teste de atualização renovando TTL
    def test_8_ttl_refresh_on_put():
        cache = LRUCacheTTL(max_size=2, ttl=0.2)
        cache.put("a", 1)
        time.sleep(0.1)
        cache.put("a", 2) # Atualização renova o TTL
        time.sleep(0.15)
        assert cache.get("a") == 2

    # 9. Edge case de tamanho limite igual a 0
    def test_9_zero_max_size():
        cache = LRUCacheTTL(max_size=0, ttl=10)
        cache.put("a", 1)
        assert cache.get("a") is None
        
    # 10. Teste com TTL negativo ou zero
    def test_10_negative_ttl():
        cache = LRUCacheTTL(max_size=2, ttl=-1)
        cache.put("a", 1)
        assert cache.get("a") is None

    tests = [
        test_1_basic_put_get, test_2_lru_eviction, test_3_ttl_expiration, test_4_lru_update,
        test_5_invalid_types_exceptions, test_6_thread_safety, test_7_empty_key, 
        test_8_ttl_refresh_on_put, test_9_zero_max_size, test_10_negative_ttl
    ]
    
    for test in tests:
        try:
            res = test()
            if res is not False:
                tests_passed += 1
        except Exception as e:
            pass
            
    return tests_passed, total_tests

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results = []
    
    for modelo in MODELOS:
        modelo_dir = os.path.join(base_dir, modelo)
        algo_file = os.path.join(modelo_dir, "algoritmoteste.py")
        
        status_compilacao = "Falha"
        tests_passed = 0
        total_tests = 10
        tempo_ms = 0.0
        memoria_kb = 0.0
        
        if os.path.exists(algo_file):
            # Usando nome do módulo unificado
            module_name = f"algoritmoteste_{modelo.replace(' ', '_').replace('.', '_').replace('(', '').replace(')', '')}"
            spec = importlib.util.spec_from_file_location(module_name, algo_file)
            
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    # Roda em uma tentativa de carregar
                    spec.loader.exec_module(module)
                    status_compilacao = "Sucesso"
                    
                    tracemalloc.start()
                    start_time = time.perf_counter()
                    
                    tests_passed, total_tests = run_tests(module)
                    
                    end_time = time.perf_counter()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    tempo_ms = (end_time - start_time) * 1000
                    memoria_kb = peak / 1024
                    
                except Exception as e:
                    status_compilacao = "Erro_Execucao"
            else:
                status_compilacao = "Erro_Importacao"
        else:
            status_compilacao = "Nao_Encontrado"
            
        results.append({
            "modelo": modelo,
            "testes_passados": tests_passed,
            "total_testes": total_tests,
            "tempo_execucao_ms": round(tempo_ms, 2),
            "memoria_pico_kb": round(memoria_kb, 2),
            "status_compilacao": status_compilacao
        })
        
    # Escreve arquivo CSV final
    csv_file = os.path.join(base_dir, "resultado.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "modelo", "testes_passados", "total_testes", 
            "tempo_execucao_ms", "memoria_pico_kb", "status_compilacao"
        ])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"Benchmark finalizado. Resultados gravados em {csv_file}")
    
    # Limpeza obrigatória do cache
    clean_cache(base_dir)

if __name__ == "__main__":
    main()
