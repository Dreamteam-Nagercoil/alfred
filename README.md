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
