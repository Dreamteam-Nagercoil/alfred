# Alfred


Alfred is an AI-powered productivity and workflow automation platform designed to simplify complex organizational workflows. It combines task management, AI agents, automation pipelines, and isolated developer workspaces into a single unified system.

The goal of Alfred is to reduce operational overhead by automating repetitive tasks while keeping humans in control of critical decisions.

> Try it out in our Azure deployment: https://opencode-workspace.wonderfulbay-2460ec53.centralindia.azurecontainerapps.io/
> The root path directs to the VSCode web. For Vikunja and Opencode, navigate to [/vikunja](https://opencode-workspace.wonderfulbay-2460ec53.centralindia.azurecontainerapps.io/vikunja) and [/opencode](https://opencode-workspace.wonderfulbay-2460ec53.centralindia.azurecontainerapps.io/opencode) respectively.

> OpenCode Access Credentials: **Username:** arthur **Password:** oxfordsnotbrogues.

> **Note:** For the demo deployment, we are using a free API from Google AI studio (though you can replace it with Ollama, or anything in the actual software, if you are running it locally on your own machine). We kindly ask you to refrain from overusing it since we are just a bunch of college students with hundreds of rupees of pocket money per month 🥲🥲

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

- OpenCode MCP client
- Any model supported by Opencode
- MCP Integrations
 > Gemini API is used for prototyping purpose


### Hosting Environment

- WSL2 Ubuntu (if running Windows)
- Ubuntu (preferred)
- Docker Runtime

---

## Installation Guide

### Prerequisites

#### In Windows

- Windows 10/11
- WSL2 Enabled

#### Software Requirements

- Docker Desktop, with WSL2 integration
- Ubuntu (WSL)
- Python 3.10+
- Git

#### In Linux
- Docker
- Docker compose
- Python (3.10+)
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
---
### Step 4: Configure Environment Variables

Rename `.env.example` into `.env`
```
cp .env.example .env
```
and add the Gemini API and Tenant's path

---
### Step 4: Build the Docker image
> Make sure docker-ce, and docker compose along with their dependecies are installed. If using Windows, make sure you are using Docker on WSL and not Docker on Windows.

```
docker build -t alfred:latest .
```


### Step 5: Launch Alfred

Start FastAPI:

```bash
cd backend/
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

# Usage

## Provisioning a Developer Environment

Using Alfred begins with the creation of a dedicated developer sandbox. An administrator accesses the FastAPI interface, enters the developer's information, the port for each service (Vikunja, VSCode Web, and Opencode) and provisions a new environment. Once submitted, Alfred automatically generates the required credentials, creates isolated storage, deploys the necessary Docker containers, and configures all supporting services.

Within a few moments, the developer receives access to a complete workspace containing a browser-based VS Code environment, a Vikunja project management workspace, and an AI agent.

A separate project inside Vijunja is created called "Opencode projects" in which the user can create any tasks that will be automated using Opencode. 

---

## AI-Powered Task Execution Workflow

Alfred goes beyond simply providing a development environment. It establishes a direct connection between project management and software development.

Developers can create and manage tasks through Vikunja, just as they would in a traditional project management system. However, when a new task is added, Alfred's AI workflow analyzes the task description and determines the required implementation.

The agent then generates relevant code, boilerplate structures, configuration files, or implementation suggestions based on the task requirements. These generated artifacts are automatically made available inside the developer's VS Code workspace, allowing the developer to immediately review, modify, and continue development.

For example, if a task such as:

> Create a FastAPI endpoint for user authentication

is added to Vikunja, the AI agent can generate the initial API structure, route definitions, request models, and supporting files directly within the development environment. The developer can then refine the generated code instead of starting from scratch.

Once code has been generated or modified, developers can continue working inside the browser-based VS Code environment. Progress can be tracked through Vikunja, while the OpenCode agent remains available to assist with implementation, debugging, documentation, and automation tasks.

By keeping task management, AI assistance, and software development within a single platform, Alfred reduces context switching and helps teams move from idea to implementation significantly faster.


## Future Scope

Alfred was developed as a proof of concept for a larger productivity ecosystem, and several improvements are planned for future iterations of the platform.

One major enhancement would be support for multiple concurrent developer environments, allowing organizations to provision isolated workspaces for entire teams rather than a single user. This would transform Alfred from a sandbox orchestration platform into a complete workspace management solution.

The AI workflow can also be expanded significantly. Future versions of Alfred could continuously monitor project progress, break down large requirements into smaller actionable tasks, automatically generate implementation plans, and assist developers throughout the entire software development lifecycle.

To improve deployment flexibility, Alfred can be integrated with cloud platforms and container orchestration solutions, enabling organizations to deploy and manage environments at scale while maintaining isolation and security.

Another area of expansion involves deeper integration with organizational resources. By connecting to internal documentation, knowledge bases, communication platforms, and repositories, Alfred could build a richer organizational knowledge graph and provide more accurate, context-aware assistance.

We would also like to create a dashboard from which an administrator can view the AI API usage, resource utilization of individual docker containers and calculate the cost of running them. 

Finally, support for self-hosted language models and custom AI agents would allow organizations to retain complete control over their data while tailoring Alfred's capabilities to their own workflows, tools, and business requirements.


## Conclusion

Alfred was created with a simple goal: let people focus on meaningful work while automation handles the overhead.

Instead of forcing users to jump between project management tools, development environments, documentation systems, and AI assistants, Alfred brings everything together into a unified workflow. A task can become a plan, a plan can become code, and code can become a completed solution—all within the same ecosystem.

While this project is only the beginning, it demonstrates how AI, automation, and modern cloud technologies can work together to reduce friction in everyday workflows and enable teams to achieve more with less effort.

Alfred is not just a productivity tool—it is our vision of a future where technology works alongside people, helping them create, collaborate, and innovate more effectively.


---

## Team Four Sure

### Project Alfred

*"Manners Maketh Man"*
