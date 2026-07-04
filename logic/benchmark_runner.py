import os
import time
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Force utf-8 e adicionar API Key
os.environ["PYTHONIOENCODING"] = "utf-8"
# Injetar a API Key do Gemini (Substitua pela sua chave no ambiente ou .env)
# os.environ["GEMINI_API_KEY"] = "SUA_CHAVE_AQUI"

BASE_DIR = "C:/Users/VSenna/testeopencode"
PROMPT = """Implemente em Python (3.10+) uma classe LRUCacheTTL thread-safe. Ela deve ter limite máximo de itens (descarte LRU) e tempo de expiração (TTL em segundos) por chave. Trate explicitamente tipos inválidos na entrada com exceções customizadas. O arquivo deve conter apenas o código da classe sem dependências externas além da biblioteca padrão. NÃO coloque texto extra, apenas código python.
MUITO IMPORTANTE: VOCÊ ESTÁ PROIBIDO DE USAR FERRAMENTAS PARA CRIAR OU SALVAR ARQUIVOS NO DISCO. VOCÊ DEVE RESPONDER COM O CÓDIGO DIRETAMENTE NO CHAT CERCADO POR ```python E ```. QUALQUER TEXTO FORA DO BLOCO DE CÓDIGO (EX: RACIOCÍNIO, AVISOS) CAUSARÁ ERRO FATAL."""

MODELOS = {
    "North Mini Code Free": "opencode/north-mini-code-free",
    "Nemotron 3 Ultra Free": "opencode/nemotron-3-ultra-free",
    "DeepSeek V4 Flash Free": "opencode/deepseek-v4-flash-free",
    "MiMo V2.5 Free": "opencode/mimo-v2.5-free",
    "Laguna XS 2.1 (free)": "openrouter/poolside/laguna-xs-2.1:free",
    "North Mini Code (free)": "openrouter/cohere/north-mini-code:free",
    "Nemotron 3 Ultra (free)": "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free",
    "Nemotron 3.5 Content Safety (free)": "openrouter/nvidia/nemotron-3.5-content-safety:free",
    "Laguna M.1 (free)": "openrouter/poolside/laguna-m.1:free",
    "Laguna XS.2 (free)": "openrouter/poolside/laguna-xs.2:free",
    "Nemotron 3 Nano Omni (free)": "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "Gemma 4 26B A4B (free)": "openrouter/google/gemma-4-26b-a4b-it:free",
    "Gemma 4 31B (free)": "openrouter/google/gemma-4-31b-it:free",
    "Nemotron 3 Super (free)": "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
    "Gemini 3.1 Flash Lite Preview": "openrouter/google/gemini-3.1-flash-lite-preview",
    "Free Models Router": "openrouter/openrouter/free",
    "LFM2.5-1.2B-Instruct (free)": "openrouter/liquid/lfm-2.5-1.2b-instruct:free",
    "LFM2.5-1.2B-Thinking (free)": "openrouter/liquid/lfm-2.5-1.2b-thinking:free",
    "Gemini 3 Flash Preview": "openrouter/google/gemini-3-flash-preview",
    "Nemotron 3 Nano 30B A3B (free)": "openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
    
    # Novos modelos Google e Previews
    "Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Gemini 2.5 Flash Lite": "google/gemini-2.5-flash-lite",
    "Gemini 2.5 Pro": "google/gemini-2.5-pro",
    "Gemini 3.5 Flash": "google/gemini-3.5-flash",
    "Gemini Flash Latest": "google/gemini-flash-latest",
    "Gemini 3 Flash Prev (Nat)": "google/gemini-3-flash-preview",
    "Gemini 3.1 Pro Prev (Nat)": "google/gemini-3.1-pro-preview",
    "Gemini 3.1 Flash Lite Prev (Nat)": "google/gemini-3.1-flash-lite-preview",
    "Gemma 4 31B (Nat)": "google/gemma-4-31b-it",
    "Gemma 4 26B A4B (Nat)": "google/gemma-4-26b-a4b-it"
}

def extract_python_code(output):
    match = re.search(r'```python\s*(.*?)\s*```', output, re.DOTALL)
    if match:
        return match.group(1).strip()
    return output.strip()

def run_model(model_name, slug):
    model_dir = os.path.join(BASE_DIR, model_name)
    os.makedirs(model_dir, exist_ok=True)
    out_file = os.path.join(model_dir, "algoritmoteste.py")
    
    # Pular se ja foi sucesso
    if os.path.exists(out_file):
        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
            if len(content.strip()) > 10 and not content.startswith("# superrequisitado"):
                print(f"[{model_name}] Ja concluido previamente.", flush=True)
                return True
    
    cmd = f'opencode.cmd run "{PROMPT}" -m {slug} --auto'
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        print(f"[{model_name}] Tentativa {attempt}/{max_retries}...", flush=True)
        try:
            # force utf-8 internally
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            process = subprocess.run(cmd, capture_output=True, text=False, timeout=300, shell=True, stdin=subprocess.DEVNULL, env=env)
            
            out_str = process.stdout.decode('utf-8', errors='replace')
            err_str = process.stderr.decode('utf-8', errors='replace')
            
            if process.returncode == 0 and len(out_str.strip()) > 10:
                code = extract_python_code(out_str)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"[{model_name}] Sucesso na tentativa {attempt}!", flush=True)
                return True
            else:
                error_msg = err_str.strip() or out_str.strip()
                print(f"[{model_name}] Falha na tentativa {attempt}. Erro: {error_msg[:100]}", flush=True)
                time.sleep(10)
                
        except subprocess.TimeoutExpired:
            print(f"[{model_name}] Timeout na tentativa {attempt}.", flush=True)
            time.sleep(10)
        except Exception as e:
            print(f"[{model_name}] Excecao na tentativa {attempt}: {e}", flush=True)
            time.sleep(10)
            
    print(f"[{model_name}] Todas as tentativas falharam. Marcando superrequisitado.", flush=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# superrequisitado\n")
    return False

def main():
    print("Iniciando orquestracao PARALELA do Benchmark com 10 workers...", flush=True)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(run_model, nome, slug): nome for nome, slug in MODELOS.items()}
        for future in as_completed(futures):
            nome = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"[{nome}] gerou excecao: {exc}", flush=True)
                
    print("Orquestracao paralela concluida!", flush=True)

if __name__ == "__main__":
    main()
