# OpenCode Platform

## Setup

1. Clone the repo
```bash
   git clone https://github.com/yourname/opencode-platform.git
   cd opencode-platform
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