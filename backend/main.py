from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
import subprocess
import uuid
import os
import httpx
import time
import json

app = FastAPI()

# AFTER (add at the very top of the file, before app = FastAPI())
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # loads .env from cwd or any parent directory

# Derived from repo structure — no need to configure this
TEMPLATE_PATH = str(Path(__file__).parent.parent / "templates" / "user-template.yml")

TENANTS_BASE   = os.getenv("TENANTS_BASE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TENANTS_BASE or not GEMINI_API_KEY:
    print("ERROR: TENANTS_BASE and GEMINI_API_KEY must be set. Copy .env.example to .env and fill it in.")
    sys.exit(1)

def vikunja_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

def create_vikunja_user(base_url: str, username: str, password: str, email: str):
    r = httpx.post(f"{base_url}/api/v1/register", json={"username": username, "password": password, "email": email}, timeout=5.0)
    if r.status_code not in (200, 201): raise Exception(f"Vikunja user creation failed: {r.text}")
    return r.json()

def get_vikunja_user_token(base_url: str, username: str, password: str) -> str:
    r = httpx.post(f"{base_url}/api/v1/login", json={"username": username, "password": password}, timeout=5.0)
    if r.status_code != 200: raise Exception(f"Vikunja login failed: {r.text}")
    return r.json()["token"]

def create_vikunja_project(base_url: str, user_token: str, name: str) -> int:
    r = httpx.put(f"{base_url}/api/v1/projects", headers=vikunja_headers(user_token), json={"title": name, "description": "Tasks here are handled by OpenCode agent"}, timeout=5.0)
    if r.status_code not in (200, 201): raise Exception(f"Vikunja project creation failed: {r.text}")
    return r.json()["id"]

def create_vikunja_webhook(base_url: str, user_token: str, project_id: int, webhook_url: str):
    r = httpx.put(f"{base_url}/api/v1/projects/{project_id}/webhooks", headers=vikunja_headers(user_token), json={"target_url": webhook_url, "events": ["task.created", "task.updated"]}, timeout=5.0)
    if r.status_code not in (200, 201): raise Exception(f"Vikunja webhook creation failed: {r.text}")
    return r.json()

def wait_for_vikunja(url: str, retries: int = 20, delay: float = 2.0) -> bool:
    for i in range(retries):
        try:
            r = httpx.get(f"{url}/api/v1/info", timeout=2.0)
            if r.status_code == 200: return True
        except httpx.RequestError: pass
        print(f"Waiting for Vikunja... attempt {i+1}/{retries}")
        time.sleep(delay)
    return False

def run_compose(env: dict, extra_args: list = []):
    cmd = ["docker", "compose", "-f", TEMPLATE_PATH, "-p", env["USER_ID"], "up", "-d"] + extra_args
    return subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

def write_container_config(container_name: str, token: str):
    config_json = json.dumps({"vikunja_token": token})
    subprocess.run(["docker", "exec", container_name, "sh", "-c", f"mkdir -p /opt/config && cat > /opt/config/config.json <<'EOF'\n{config_json}\nEOF"], check=True)

@app.get("/", response_class=HTMLResponse)
def admin_panel():
    return """
    <html>
        <head>
            <title>OpenCode Multi-Tenant Orchestrator</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #0f172a; color: #f8fafc; }
                .card { background: #1e293b; padding: 30px; border-radius: 12px; max-width: 520px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); margin: auto; }
                input { width: 100%; padding: 10px; margin: 8px 0 18px 0; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
                input[type="submit"] { background: #3b82f6; border: none; font-weight: bold; cursor: pointer; transition: 0.2s; margin-top: 10px; }
                input[type="submit"]:hover { background: #2563eb; }
                h2 { color: #3b82f6; text-align: center; margin-top: 0; }
                label { font-weight: 600; color: #94a3b8; font-size: 14px; }
                .row { display: flex; gap: 15px; }
                .col { flex: 1; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Deploy Developer Sandbox</h2>
                <form action="/create-env" method="post">
                    <label>Developer Username:</label>
                    <input type="text" name="username" placeholder="e.g. alice" required>
                    <label>Email:</label>
                    <input type="email" name="email" placeholder="e.g. alice@example.com" required>
                    
                    <div class="row">
                        <div class="col">
                            <label>VS Code Web Port:</label>
                            <input type="number" name="opencode_port" placeholder="e.g. 4455" min="1024" max="65535" required>
                        </div>
                        <div class="col">
                            <label>OpenCode UI Port:</label>
                            <input type="number" name="agent_ui_port" placeholder="e.g. 4466" min="1024" max="65535" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col">
                            <label>Vikunja Port:</label>
                            <input type="number" name="vikunja_port" placeholder="e.g. 3500" min="1024" max="65535" required>
                        </div>
                    </div>
                    <input type="submit" value="Provision Sandbox">
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/create-env")
def create_env(
    username: str = Form(...),
    email: str = Form(...),
    opencode_port: int = Form(...),
    agent_ui_port: int = Form(...),
    vikunja_port: int = Form(...)
):
    clean_username = "".join(c for c in username if c.isalnum() or c in ("_", "-")).lower()
    if not clean_username: raise HTTPException(status_code=400, detail="Invalid username")

    user_id = f"user_{clean_username}"
    webhook_port = opencode_port + 1000

    vikunja_password = uuid.uuid4().hex[:12]
    server_pass = uuid.uuid4().hex[:10]
    host_base_path = f"{TENANTS_BASE}/{user_id}"
    host_data_path = f"{host_base_path}/data"

    try:
        os.makedirs(host_data_path, exist_ok=True)

        base_env = {
            **os.environ,
            "USER_ID": user_id,
            "SERVER_PASS": server_pass,
            "OPENCODE_PORT": str(opencode_port),
            "AGENT_UI_PORT": str(agent_ui_port),
            "VIKUNJA_PORT": str(vikunja_port),
            "WEBHOOK_PORT": str(webhook_port),
            "HOST_DATA_PATH": host_data_path,
            "GEMINI_API_KEY": GEMINI_API_KEY,
            "VIKUNJA_OUTGOINGREQUESTS_ALLOWNONROUTABLEIPS": "true"
        }

        run_compose(base_env, ["--force-recreate"])
        vikunja_url = f"http://localhost:{vikunja_port}"

        if not wait_for_vikunja(vikunja_url):
            raise Exception(f"Vikunja did not start on port {vikunja_port} in time.")

        create_vikunja_user(vikunja_url, clean_username, vikunja_password, email)
        user_token = get_vikunja_user_token(vikunja_url, clean_username, vikunja_password)
        project_id = create_vikunja_project(vikunja_url, user_token, "OpenCode Projects")
        create_vikunja_webhook(vikunja_url, user_token, project_id, "http://127.0.0.1:5000/webhook")

        container_name = f"{user_id}-env"
        write_container_config(container_name, user_token)

        return {
            "status": "success",
            "developer": clean_username,
            "environment_id": user_id,
            "connection_details": {
                "vscode_web_ui": f"http://localhost:{opencode_port}",
                "opencode_task_control_ui": f"http://localhost:{agent_ui_port}",
                "opencode_username": user_id,       # FIX: Prints the server username
                "opencode_password": server_pass,    # FIX: Prints the generated token
                "vikunja_web_ui": f"http://localhost:{vikunja_port}",
                "vikunja_username": clean_username,
                "vikunja_password": vikunja_password
            }
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail={"returncode": e.returncode, "stdout": e.stdout, "stderr": e.stderr})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestration error: {str(e)}")