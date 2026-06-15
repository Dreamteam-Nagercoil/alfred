FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    openssh-server \
    python3 \
    python3-pip \
    python3-venv \
    xdg-utils \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Setup Python environment setup
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install fastapi uvicorn httpx

RUN curl -fsSL https://opencode.ai/install | bash \
    && chmod +x /root/.opencode/bin/opencode

RUN curl -L -o /tmp/vikunja.zip \
    https://dl.vikunja.io/vikunja/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip \
    && unzip /tmp/vikunja.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/vikunja-v2.3.0-linux-amd64 /usr/local/bin/vikunja \
    && chmod +x /usr/local/bin/vikunja \
    && rm /tmp/vikunja.zip

ENV PATH="/root/.opencode/bin:${PATH}"

RUN mkdir -p \
    /root/.config/opencode \
    /opt/vikunja/data \
    /opt/vikunja/files \
    /opt/config

COPY webhook-receiver/receiver.py /opt/receiver.py
COPY start.sh /opt/start.sh

RUN chmod +x /opt/start.sh
RUN curl -fsSL https://code-server.dev/install.sh | sh

ENTRYPOINT ["/opt/start.sh"]