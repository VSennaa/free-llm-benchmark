#!/bin/bash

# Script orquestrador para invocar os modelos e gerar os arquivos algoritmoteste.py

BASE_DIR="C:/Users/VSenna/testeopencode"
PROMPT="Você deve implementar em Python (3.10+) uma classe \`LRUCacheTTL\` thread-safe. Ela deve ter limite máximo de itens (descarte LRU) e tempo de expiração (TTL em segundos) por chave. Trate explicitamente tipos inválidos na entrada com exceções customizadas. O arquivo deve conter apenas o código da classe (e dependências da Standard Library do Python)."

MODELOS=(
    "North Mini Code Free"
    "Nemotron 3 Ultra Free"
    "DeepSeek V4 Flash Free"
    "MiMo V2.5 Free"
    "Laguna XS 2.1 (free)"
    "North Mini Code (free)"
    "Nemotron 3 Ultra (free)"
    "Nemotron 3.5 Content Safety (free)"
    "Laguna M.1 (free)"
    "Laguna XS.2 (free)"
    "Nemotron 3 Nano Omni (free)"
    "Gemma 4 26B A4B (free)"
    "Gemma 4 31B (free)"
    "Nemotron 3 Super (free)"
    "Gemini 3.1 Flash Lite Preview"
    "Free Models Router"
    "LFM2.5-1.2B-Instruct (free)"
    "LFM2.5-1.2B-Thinking (free)"
    "Gemini 3 Flash Preview"
    "Nemotron 3 Nano 30B A3B (free)"
)

# Cria a pasta base
mkdir -p "$BASE_DIR"

for MODELO in "${MODELOS[@]}"; do
    # Usando string exata para a pasta do modelo
    MODELO_DIR="$BASE_DIR/$MODELO"
    mkdir -p "$MODELO_DIR"
    
    ALGO_FILE="$MODELO_DIR/algoritmoteste.py"
    
    echo "=========================================="
    echo "Processando Modelo: $MODELO"
    echo "=========================================="
    
    # Chamada real para a CLI do antigravity. 
    # O output padrao sera direcionado para algoritmoteste.py do respectivo modelo.
    # Pode ser necessario formatar o output se o modelo retornar markdown usando sed/awk,
    # ou usar a funcionalidade nativa do antigravity se existir algo como '--format python'.
    
    # Exemplo simulado da chamada. 
    # Modifique essa chamada conforme a syntax exata do antigravity CLI disponível
    # antigravity ask --model "$MODELO" "$PROMPT" > "$ALGO_FILE"
    
    # Gerando um template provisório apenas para estrutura:
    cat <<EOF > "$ALGO_FILE"
# TODO: Substituir este conteudo pela implementacao real do modelo via antigravity CLI
# Modelo: $MODELO
class LRUCacheTTL:
    def __init__(self, max_size, ttl):
        pass
    def put(self, key, value):
        pass
    def get(self, key):
        pass
EOF

done

echo ""
echo "Estrutura do Benchmark criada."
echo "Para avaliar os modelos gerados, execute o script em python:"
echo "python $BASE_DIR/avaliador.py"
