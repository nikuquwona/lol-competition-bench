FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tmux asciinema && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home agent && mkdir -p /app && chown agent:agent /app
WORKDIR /app
COPY snapshot.json /app/snapshot.json
