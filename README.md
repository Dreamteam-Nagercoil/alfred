# Alfred

## Setup

1. Clone the repo
```bash
   git clone https://github.com/Dreamteam-Nagercoil/alfred.git
   cd alfred/
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Configure environment
```bash
   cp .env.example .env
   # Edit .env and fill in GEMINI_API_KEY and TENANTS_BASE
```

4. Build the Docker image
```bash
   docker build -t opencode-sandbox .
```

5. Run the orchestrator
```bash
   uvicorn backend.main:app --reload
```


# Alfred

## Overview

Alfred is an AI-powered productivity and workflow automation platform designed to simplify complex organizational workflows. It combines task management, AI agents, automation pipelines, and isolated developer workspaces into a single unified system.

The goal of Alfred is to reduce operational overhead by automating repetitive tasks while keeping humans in control of critical decisions.

---

## Problem Statement
Build innovative software solutions that redefine how people work, collaborate, create, and manage their daily workflows. The project should focus on improving productivity for individuals, teams, startups, creators, developers, designers, or businesses using modern technologies such as Artificial Intelligence, automation, cloud systems, or smart integrations.


## Features

### Developer Sandbox Provisioning

Provision complete development environments with a single click.

Each environment includes:

- VS Code Online
- Vikunja Task Manager
- OpenCode Agent
- Persistent Storage

---

### AI Assisted Workflow Automation

Alfred leverages AI-powered workflows to:

- Process user requests
- Manage repetitive tasks
- Assist in task execution
- Generate outputs efficiently

---

### Task Management

Integrated with Vikunja to provide:

- Project Management
- Task Assignment
- Progress Tracking
- Workflow Monitoring

---

### Container Isolation

Each workspace is provisioned inside isolated Docker containers, ensuring:

- Separation of environments
- Better security
- Easy maintenance
- Improved portability

---

## Technology Stack

### Backend

- Python
- FastAPI
- HTTPX

### Containerization

- Docker
- Docker Compose

### Productivity Tools

- Vikunja

### Development Environment

- VS Code Server

### AI Layer

- Gemini API
- MCP Integrations

### Hosting Environment

- WSL2 Ubuntu
- Docker Runtime

---

## Installation Guide

### Prerequisites

#### In Windows

- Windows 10/11
- WSL2 Enabled

#### Software Requirements

- Docker Desktop
- Ubuntu (WSL)
- Python 3.10+
- Git

---

### Step 1: Clone Repository

```bash
git clone https://github.com/Dreamteam-Nagercoil/alfred.git
cd alfred
```

---

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
# and activate it
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If required:

```bash
pip install python-multipart
```

### Step 4: Configure Environment Variables

Edit .env and fill in GEMINI_API_KEY and TENANTS_BASE

### Step 5: Launch Alfred

Start FastAPI:

```bash
uvicorn backend.main:app --reload
```

Expected Output:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

Open:

```text
http://localhost:8000
```

---
