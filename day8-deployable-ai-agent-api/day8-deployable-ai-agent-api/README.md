# Day 8 Lab — Deployable AI Agent API with FastAPI, Docker, and Ollama

## Goal

In this lab, we turn a local Ollama-powered AI agent into a web API.

By the end, learners will have a deployable FastAPI project with:

- A `/health` endpoint
- A `/chat` endpoint
- An Ollama model connection
- A `Dockerfile`
- A `docker-compose.yml` file

## Final architecture

```text
User or frontend
  -> FastAPI /chat endpoint
  -> Ollama host
  -> Local model response
  -> JSON response
```

## Why this matters

A local chatbot is useful for learning, but real applications usually need an API.

An API lets another app, website, frontend, or automation call the AI agent over HTTP.
That is the main step from local prototype to deployable application.

## Project structure

```text
day8-deployable-ai-agent-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── ollama_client.py
│   └── schemas.py
├── scripts/
│   └── test_api.sh
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Important note about Ollama and cloud deployment

Ollama runs as a local service by default.

For true cloud deployment, the FastAPI app must be able to reach an Ollama server.
That can be:

1. Ollama running on the same cloud virtual machine
2. Ollama running in Docker Compose beside the app
3. A remote Ollama host that the app can access

For this beginner lab, we make the app cloud-ready and run everything locally with Docker Compose.

## Option 1 — Run locally without Docker

Use this option when teaching the code first.

### 1. Go to the project folder

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day8-deployable-ai-agent-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

In another terminal:

```bash
ollama serve
```

If Ollama is already running as a background service, this command may say the port is already in use. That is okay.

### 5. Pull the model

```bash
ollama pull llama3.2:1b
```

### 6. Start the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Open the API docs

Go to:

```text
http://localhost:8000/docs
```

## Option 2 — Run with Docker Compose

Use this option when teaching deployment readiness.

### 1. Start the services

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day8-deployable-ai-agent-api
docker compose up --build
```

This starts two services:

- `api`: the FastAPI application
- `ollama`: the Ollama server

### 2. Pull the model inside the Ollama container

In a second terminal:

```bash
docker compose exec ollama ollama pull llama3.2:1b
```

### 3. Test the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "app_name": "Deployable AI Agent API",
  "ollama_base_url": "http://ollama:11434",
  "model": "llama3.2:1b"
}
```

### 4. Test the chat endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain Docker in one beginner-friendly sentence."}'
```

Expected response shape:

```json
{
  "response": "...",
  "model": "llama3.2:1b"
}
```

### 5. Run the helper test script

```bash
./scripts/test_api.sh
```

## API endpoints

### `GET /health`

Confirms that the FastAPI app is running and shows the configured Ollama host and model.

### `POST /chat`

Sends a user message to the Ollama model and returns the model response as JSON.

Request body:

```json
{
  "message": "What is FastAPI?",
  "system_prompt": "You are a helpful teacher.",
  "model": "llama3.2:1b"
}
```

Only `message` is required.

## Environment variables

The app reads these values from environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `APP_NAME` | Display name for the API | `Deployable AI Agent API` |
| `OLLAMA_BASE_URL` | URL of the Ollama server | `http://localhost:11434` |
| `OLLAMA_MODEL` | Default model used by `/chat` | `llama3.2:1b` |
| `REQUEST_TIMEOUT_SECONDS` | Timeout for Ollama requests | `60` |

For local development, copy the example file:

```bash
cp .env.example .env
```

## Common beginner issues

### API works, but `/chat` fails

Most likely, Ollama is not running or the model has not been pulled yet.

For local mode:

```bash
ollama pull llama3.2:1b
```

For Docker Compose mode:

```bash
docker compose exec ollama ollama pull llama3.2:1b
```

### Docker Compose starts, but the first chat request is slow

That is normal. Local models can take a little time to load into memory the first time.

### Running in the cloud

The same FastAPI app can run in the cloud, but the app must still reach an Ollama host.

For a beginner-friendly cloud setup, run both FastAPI and Ollama on the same VM or in the same Docker Compose environment.
