# SupaChat 🚀

SupaChat is a conversational analytics web app built on top of Supabase PostgreSQL and an MCP server! It uses AI to convert natural language queries into insights through table representations and visual graphs.

## Features ✨
- **Chatbot UI**: Natural conversational interface (Next.js & Tailwind).
- **Interactive Graphs**: Real-time rendering via Recharts.
- **LLM/MCP backend**: Powered by FastAPI, querying Supabase using dynamic mappings based on conversational intents.
- **Full DevOps Lifecycle**: 
  - Docker & Docker Compose setup
  - Nginx Reverse proxy with Gzip & caching
  - CI/CD via GitHub Actions (EC2 Deployment Script)
  - Complete Monitoring Stack (Prometheus, Grafana, Loki, Promtail)

## Architecture 🏛️
1. **Frontend**: Next.js 14, React, Tailwind, Lucide Icons, Recharts.
2. **Backend**: Python FastAPI, OpenAI API, Supabase connection.
3. **Infrastructure**: Docker orchestrating all microservices inside isolated environments locally and in EC2.

## How to Run Locally 💻

### Prerequisites
- Docker & Docker Compose installed.
- A Supabase Project with `articles` and `metrics` tables (Use the `backend/schema.sql` and `backend/seed.sql` to initialize it).
- A Gemini API Key.

### Steps
1. **Set Environment Variables**: Create a `.env` file in the root or export variables directly:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   export SUPABASE_URL="https://your-project.supabase.co"
   export SUPABASE_KEY="your-anon-key"
   ```

2. **Docker Compose Up**:
   ```bash
   docker-compose up -d --build
   ```

3. **Access the App**:
   - Web UI: http://localhost:80 (Served by Nginx)
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (User: admin / Pass: admin)
     - You can add Loki (`http://loki:3100`) and Prometheus (`http://prometheus:9090`) as data sources inside Grafana.

## CI/CD 🤖
This project contains a GitHub Actions workflow (`.github/workflows/deploy.yml`) that triggers on push to the `main` branch.
It SSHs into your configured EC2 instance, pulls the latest code, injects API secrets as environment variables, and executes `docker-compose up -d --build` for a seamless deployment.

Required GitHub Secrets:
- `EC2_SSH_KEY`, `EC2_USER`, `EC2_HOST`
- `GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

## AI Tools Used
This project was vibe-coded using Agentic AI workflows to rapidly scaffold frontend applications, build complex FastAPI controllers, and configure robust docker/monitoring configurations.
