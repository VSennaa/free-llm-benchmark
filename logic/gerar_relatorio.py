import csv
import os

BASE_DIR = "C:/Users/VSenna/testeopencode"
CSV_FILE = os.path.join(BASE_DIR, "resultado.csv")
REPORT_FILE = os.path.join(BASE_DIR, "docs/report.md")

def gerar_relatorio():
    if not os.path.exists(CSV_FILE):
        print("CSV não encontrado.")
        return

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    
    resultados = []
    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            resultados.append(row)
            
    # Metodologia Fábio Akita adaptada:
    # 0 a 100 pontos.
    # - Compilação/Encontrado: Base
    # - 10 Testes (5 pontos por teste passado = até 50 pontos)
    # - Eficiência: Memória (até 15 pontos) e Tempo (até 15 pontos)
    # - Código correto sem erro de importação/execução: (20 pontos)
    # Modelos "superrequisitado" (Falha / Não Encontrado) = 0 pontos
    
    # Calcular Max Time e Max Mem para normalização
    tempos = [float(r['tempo_execucao_ms']) for r in resultados if float(r['tempo_execucao_ms']) > 0]
    mems = [float(r['memoria_pico_kb']) for r in resultados if float(r['memoria_pico_kb']) > 0]
    
    max_time = max(tempos) if tempos else 1
    max_mem = max(mems) if mems else 1
    
    rankings = []
    
    for r in resultados:
        modelo = r['modelo']
        status = r['status_compilacao']
        testes_passados = int(r['testes_passados'])
        tempo_ms = float(r['tempo_execucao_ms'])
        mem_kb = float(r['memoria_pico_kb'])
        
        nota = 0
        analise_erros = ""
        
        if status in ["Falha", "Nao_Encontrado", "Erro_Importacao"]:
            nota = 0
            analise_erros = "Modelo falhou por não gerar código válido ou sobrecarga de fila (superrequisitado)."
        elif status == "Erro_Execucao":
            nota = testes_passados * 5
            analise_erros = "Código gerado quebrou durante a execução de alguns testes (Exceptions)."
        else:
            # Sucesso básico: 20 pontos
            nota += 20
            # Testes: até 50 pontos
            nota += (testes_passados * 5)
            # Normalização de eficiência
            # Menor tempo = mais pontos
            pontos_tempo = 15 * (1 - (tempo_ms / max_time))
            # Menor mem = mais pontos
            pontos_mem = 15 * (1 - (mem_kb / max_mem))
            
            nota += max(0, pontos_tempo)
            nota += max(0, pontos_mem)
            
            if testes_passados == 10:
                analise_erros = "Código impecável. Passou em 100% dos testes da suíte rigorosa."
            else:
                analise_erros = f"Pequenos bugs. Passou em {testes_passados}/10 testes."
                
        rankings.append({
            "modelo": modelo,
            "nota": round(nota, 2),
            "testes_passados": testes_passados,
            "tempo_execucao_ms": tempo_ms,
            "memoria_pico_kb": mem_kb,
            "analise_erros": analise_erros,
            "status": status
        })
        
    # Ordenar por nota descendente
    rankings.sort(key=lambda x: x['nota'], reverse=True)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Relatório Final do Benchmark LLM (Metodologia Akita Adaptada)\n\n")
        f.write("Este relatório aplica uma escala holística de 0 a 100 baseada na metodologia de Fábio Akita, considerando corretude, tratamento de exceções (testes) e eficiência (Pico de Memória e Tempo).\n\n")
        f.write("## Ranking\n\n")
        f.write("| Posição | Modelo | Nota (0-100) | Testes (0-10) | Memória (KB) | Tempo (ms) | Status |\n")
        f.write("|---------|--------|--------------|---------------|--------------|------------|--------|\n")
        
        for i, r in enumerate(rankings):
            f.write(f"| {i+1} | **{r['modelo']}** | {r['nota']} | {r['testes_passados']} | {r['memoria_pico_kb']:.2f} | {r['tempo_execucao_ms']:.2f} | {r['status']} |\n")
            
        f.write("\n## Análise Individual\n\n")
        for i, r in enumerate(rankings):
            f.write(f"### {i+1}. {r['modelo']}\n")
            f.write(f"- **Nota Final:** {r['nota']}\n")
            f.write(f"- **Análise dos Erros:** {r['analise_erros']}\n")
            f.write("\n")
            
    print(f"Relatório gerado em: {REPORT_FILE}")

if __name__ == "__main__":
    gerar_relatorio()
