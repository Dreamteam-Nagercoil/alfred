FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install baseline requirements + Nginx
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    openssh-server \
    python3 \
    python3-pip \
    python3-venv \
    xdg-utils \
    unzip \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install code-server (VS Code Web Interface)
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Setup Python environment setup
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install fastapi uvicorn httpx

# Install OpenCode Binary
RUN curl -fsSL https://opencode.ai/install | bash \
    && chmod +x /root/.opencode/bin/opencode
ENV PATH="/root/.opencode/bin:${PATH}"

# Install Vikunja
RUN curl -L -o /tmp/vikunja.zip \
    https://dl.vikunja.io/vikunja/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip \
    && unzip /tmp/vikunja.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/vikunja-v2.3.0-linux-amd64 /usr/local/bin/vikunja \
    && chmod +x /usr/local/bin/vikunja \
    && rm /tmp/vikunja.zip

RUN mkdir -p /root/.config/opencode /opt/vikunja/data /opt/vikunja/files /opt/config

# Copy components and reverse proxy config
COPY nginx.conf /etc/nginx/nginx.conf
COPY webhook-receiver/receiver.py /opt/receiver.py
COPY start.sh /opt/start.sh

RUN chmod +x /opt/start.sh

# Expose Nginx port only
EXPOSE 80

ENTRYPOINT ["/opt/start.sh"]