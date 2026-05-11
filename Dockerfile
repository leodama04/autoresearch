FROM nvidia/cuda:12.4.0-devel-ubuntu22.04

LABEL maintainer="UniboNLP"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y \
    curl \
    git \
    bash \
    nano \
    python3.11 \
    python3.11-dev \
    python3-pip \
    build-essential \
    zstd \
    libcudnn9-cuda-12 && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install wrapt --upgrade --ignore-installed

# uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

ENV DEBIAN_FRONTEND=dialog

WORKDIR /app
COPY . .
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]