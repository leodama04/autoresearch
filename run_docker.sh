#!/bin/bash

PHYS_DIR="$HOME/autoresearch"

docker run \
    -v "$PHYS_DIR":/app \
    -v "$PHYS_DIR/program.md":/program.md \ 
    -v ollama_data:/root/.ollama \
    -v cache_data:/root/.cache/autoresearch \
    --rm \
    --memory="30g" \
    --gpus '"device='"$CUDA_VISIBLE_DEVICES"'"' \
    --env OLLAMA_HOST=http://localhost:11434 \
    --env NVIDIA_VISIBLE_DEVICES=all \
    autoresearch-agent \
    "/app/entrypoint.sh"