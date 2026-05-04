#!/bin/bash
set -e

# 1. Avvia Ollama in background
ollama serve > /app/ollama.log 2>&1 &

echo "Waiting for Ollama..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 1
done
echo "Ollama ready."

# 2. uv sync
echo "Running uv sync..."
uv sync

# 3. prepare.py (download dati + training tokenizer)
echo "Running prepare.py..."
uv run prepare.py --num-shards 10

# 4. main.py (l'agente gestisce lui train.py autonomamente)
echo "Running main.py..."
uv run main.py