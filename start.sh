#!/bin/bash
set -e

mkdir -p /home/vscode/workspace
mkdir -p /root/.config/opencode
mkdir -p /opt/vikunja/data
mkdir -p /opt/vikunja/files
mkdir -p /opt/config
#!/bin/bash
set -e

mkdir -p /home/vscode/workspace /root/.config/opencode /opt/vikunja/data /opt/vikunja/files /opt/config
echo '{"$schema":"https://opencode.ai/config.json","model":"google/gemini-3.1-flash-lite"}' > /root/.config/opencode/opencode.json

export VIKUNJA_DATABASE_PATH=/opt/vikunja/data/vikunja.db
export VIKUNJA_FILES_BASEPATH=/opt/vikunja/files
export VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/
export VIKUNJA_CORS_ENABLE=false

echo "Starting Vikunja..."
vikunja web > /var/log/vikunja.log 2>&1 &

echo "Starting Webhook Receiver..."
python3 -u /opt/receiver.py > /var/log/receiver.log 2>&1 &

echo "Starting OpenCode Web Task Control..."
export OPENCODE_USERNAME="${OPENCODE_SERVER_USERNAME}"
export OPENCODE_PASSWORD="${OPENCODE_SERVER_PASSWORD}"
/root/.opencode/bin/opencode web --port 8080 --hostname 127.0.0.1 > /var/log/opencode-web.log 2>&1 &

echo "Starting VS Code Web Server..."
# Bind code-server internally to 4096 without authentication (or modify as preferred)
code-server --bind-addr 127.0.0.1:4096 --auth none /home/vscode/workspace > /var/log/code-server.log 2>&1 &

echo "Starting Nginx Reverse Proxy Gateway Layer..."
# This command runs in the foreground so the container stays alive
exec nginx -g "daemon off;"