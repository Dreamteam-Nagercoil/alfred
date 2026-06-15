#!/bin/bash
set -e

mkdir -p /home/vscode/workspace
mkdir -p /root/.config/opencode
mkdir -p /opt/vikunja/data
mkdir -p /opt/vikunja/files
mkdir -p /opt/config
echo '{"$schema":"https://opencode.ai/config.json","model":"google/gemini-3.1-flash-lite"}' > /root/.config/opencode/opencode.json

# Gracefully handle SSH configuration only if openssh-server is available
if [ -f /etc/ssh/sshd_config ]; then
    echo "Configuring SSH services..."
    usermod --shell /bin/bash vscode || true
    echo "vscode:vscode" | chpasswd

    mkdir -p /var/run/sshd
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
    sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config || true
    sed -i 's/#ChallengeResponseAuthentication no/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config || true

    service ssh restart || service ssh start || true
else
    echo "SSH Server configuration skipped (not installed/missing config)."
fi

echo -e '#!/bin/sh\necho skip' > /usr/local/bin/xdg-open
chmod +x /usr/local/bin/xdg-open

export VIKUNJA_DATABASE_PATH=/opt/vikunja/data/vikunja.db
export VIKUNJA_FILES_BASEPATH=/opt/vikunja/files
export VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/
export VIKUNJA_CORS_ENABLE=false

echo "Starting Vikunja..."
vikunja web > /var/log/vikunja.log 2>&1 &

echo "Starting receiver..."
python3 -u /opt/receiver.py > /var/log/receiver.log 2>&1 &

# Update this block in your start.sh
echo "Starting OpenCode Web Task Control..."
export OPENCODE_USERNAME="${OPENCODE_SERVER_USERNAME}"
export OPENCODE_PASSWORD="${OPENCODE_SERVER_PASSWORD}"

/root/.opencode/bin/opencode web \
    --port 8080 \
    --hostname 0.0.0.0 > /var/log/opencode-web.log 2>&1 &

cd /home/vscode/workspace

echo "Starting VS Code Web Server..."
exec code-server --bind-addr 0.0.0.0:4096 --auth none /home/vscode/workspace