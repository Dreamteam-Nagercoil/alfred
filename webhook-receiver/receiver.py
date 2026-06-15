from fastapi import FastAPI, Request
import subprocess
import httpx
import os
import asyncio
import json

app = FastAPI()

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "http://127.0.0.1:3456")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
WORKSPACE = "/home/vscode/workspace"
CONFIG_PATH = "/opt/config/config.json"

pending_tasks = {}

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config file: {e}", flush=True)
        return {"vikunja_token": "placeholder"}

def post_comment(task_id: int, message: str):
    try:
        cfg = load_config()
        httpx.post(
            f"{VIKUNJA_URL}/api/v1/tasks/{task_id}/comments",
            headers={"Authorization": f"Bearer {cfg['vikunja_token']}"},
            json={"comment": message},
            timeout=5.0
        )
    except Exception as e:
        print(f"Failed to post comment: {e}", flush=True)


@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    event = payload.get("event_name", "")
    
    if event not in ("task.created", "task.updated"):
        return {"status": "ignored"}

    task = payload.get("data", {}).get("task", {})
    task_id = task.get("id")
    title = task.get("title", "")
    description = task.get("description", "")
    done = task.get("done", False)

    if done or not task_id or not title:
        return {"status": "ignored"}

    if event == "task.created":
        print(f"-> task.created received for ID {task_id}. Initializing debounce.", flush=True)
        pending_tasks[task_id] = {
            "title": title,
            "description": description,
            "updated_event": asyncio.Event()
        }
        asyncio.create_task(wait_and_launch_session(task_id, delay=10.0))
        return {"status": "waiting_for_potential_description", "task_id": task_id}

    elif event == "task.updated":
        if task_id in pending_tasks:
            print(f"-> task.updated received for ID {task_id}.", flush=True)
            pending_tasks[task_id]["description"] = description
            pending_tasks[task_id]["title"] = title
            if description.strip():
                pending_tasks[task_id]["updated_event"].set()
            return {"status": "updated_description_captured", "task_id": task_id}
        
        return {"status": "ignored_historical_update"}


async def wait_and_launch_session(task_id: int, delay: float):
    try:
        task_info = pending_tasks.get(task_id)
        if not task_info:
            return

        try:
            await asyncio.wait_for(task_info["updated_event"].wait(), timeout=delay)
        except asyncio.TimeoutError:
            pass

        final_task = pending_tasks.pop(task_id, None)
        if not final_task:
            return

        title = final_task["title"]
        description = final_task["description"]

        # FIX: Dynamically build an isolated environment directory for every new task
        task_folder_name = f"task-{task_id}"
        task_dir = os.path.join(WORKSPACE, task_folder_name)
        os.makedirs(task_dir, exist_ok=True)

        # Drop the context file inside the directory
        with open(os.path.join(task_dir, "INSTRUCTIONS.md"), "w") as f:
            f.write(f"# Task Context: {title}\n\n## Instructions\n{description}\n")

        prompt = f"""Task: {title}

Description:
{description}

Work inside the current working directory: {task_dir}. 
Analyze the INSTRUCTIONS.md file and create or edit files in this directory to solve the task."""

        run_env = os.environ.copy()
        run_env["GEMINI_API_KEY"] = GEMINI_KEY
        run_env["GOOGLE_GENERATIVE_AI_API_KEY"] = GEMINI_KEY
        if "PATH" not in run_env:
            run_env["PATH"] = "/root/.opencode/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

        print(f"-> Spawning isolated OpenCode task worker inside: {task_folder_name}", flush=True)
        
        # OpenCode runs standalone targeting this exact folder
        subprocess.Popen(
            [
                "/root/.opencode/bin/opencode", "run",
                "--dir", task_dir,
                "--title", f"Task #{task_id}",
                prompt
            ],
            env=run_env,
            cwd=task_dir
        )
        
        post_comment(task_id, f"📁 Isolated workspace folder environment generated at `{task_folder_name}`. System edits are processing locally inside this scope.")

    except Exception as e:
        print(f"Failed to handle task execution context: {e}", flush=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)