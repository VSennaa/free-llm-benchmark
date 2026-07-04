import importlib.util
import time
import threading

spec = importlib.util.spec_from_file_location('test', 'algoritmoteste.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

LRUCacheTTL = module.LRUCacheTTL

# Test 1
try:
    cache = LRUCacheTTL(max_size=3, ttl=10)
    cache.put('a', 1)
    assert cache.get('a') == 1
    print('Test 1: PASS')
except Exception as e:
    print(f'Test 1: FAIL - {e}')

# Test 2
try:
    cache = LRUCacheTTL(max_size=2, ttl=10)
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    assert cache.get('a') is None
    assert cache.get('b') == 2
    assert cache.get('c') == 3
    print('Test 2: PASS')
except Exception as e:
    print(f'Test 2: FAIL - {e}')

# Test 3
try:
    cache = LRUCacheTTL(max_size=2, ttl=0.1)
    cache.put('a', 1)
    time.sleep(0.15)
    assert cache.get('a') is None
    print('Test 3: PASS')
except Exception as e:
    print(f'Test 3: FAIL - {e}')

# Test 4
try:
    cache = LRUCacheTTL(max_size=2, ttl=10)
    cache.put('a', 1)
    cache.put('b', 2)
    cache.get('a')
    cache.put('c', 3)
    assert cache.get('b') is None
    assert cache.get('a') == 1
    print('Test 4: PASS')
except Exception as e:
    print(f'Test 4: FAIL - {e}')

# Test 5
try:
    cache = LRUCacheTTL(max_size=2, ttl=10)
    try:
        cache.put(None, 1)
    except:
        pass
    print('Test 5: PASS')
except Exception as e:
    print(f'Test 5: FAIL - {e}')

# Test 6
try:
    cache = LRUCacheTTL(max_size=100, ttl=10)
    def worker(i):
        cache.put(f'k{i}', i)
        cache.get(f'k{i}')
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert cache.get('k0') == 0 or cache.get('k0') is None
    print('Test 6: PASS')
except Exception as e:
    print(f'Test 6: FAIL - {e}')

# Test 7
try:
    cache = LRUCacheTTL(max_size=2, ttl=10)
    cache.put('', 'vazio')
    assert cache.get('') == 'vazio'
    print('Test 7: PASS')
except Exception as e:
    print(f'Test 7: FAIL - {e}')

# Test 8
try:
    cache = LRUCacheTTL(max_size=2, ttl=0.2)
    cache.put('a', 1)
    time.sleep(0.1)
    cache.put('a', 2)
    time.sleep(0.15)
    assert cache.get('a') == 2
    print('Test 8: PASS')
except Exception as e:
    print(f'Test 8: FAIL - {e}')

# Test 9
try:
    cache = LRUCacheTTL(max_size=0, ttl=10)
    cache.put('a', 1)
    assert cache.get('a') is None
    print('Test 9: PASS')
except Exception as e:
    print(f'Test 9: FAIL - {e}')

# Test 10
try:
    cache = LRUCacheTTL(max_size=2, ttl=-1)
    cache.put('a', 1)
    assert cache.get('a') is None
    print('Test 10: PASS')
except Exception as e:
    print(f'Test 10: FAIL - {e}')

print('ALL TESTS COMPLETE')