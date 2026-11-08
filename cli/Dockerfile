FROM node:24-bookworm-slim
ARG HARNESS
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git python3 socat && rm -rf /var/lib/apt/lists/*
RUN set -eu; case "$HARNESS" in \
 claude) npm install -g @anthropic-ai/claude-code@2.1.319 ;; \
 codex) npm install -g @openai/codex@0.167.0 ;; \
 pi) npm install -g @earendil-works/pi-coding-agent@1.5.0 ;; \
 kimi) npm install -g @moonshot-ai/kimi-code@2.5.2 ;; \
 cursor) arch="$(dpkg --print-architecture)"; case "$arch" in amd64) arch=x64;; arm64) arch=arm64;; *) exit 2;; esac; mkdir /opt/cursor; curl -fsSL --retry 3 "https://downloads.cursor.com/lab/2026.11.05-86047df/linux/$arch/agent-cli-package.tar.gz" | tar -xz --strip-components=1 -C /opt/cursor; ln -s /opt/cursor/cursor-agent /usr/local/bin/cursor-agent ;; \
 *) exit 2 ;; esac
COPY client.py /opt/bench/client.py
WORKDIR /app
USER node
