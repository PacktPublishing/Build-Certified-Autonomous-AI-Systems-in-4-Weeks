from fastapi import FastAPI, HTTPException

from app.config import settings
from app.ollama_client import OllamaError, ask_ollama
from app.schemas import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(
    title=settings.app_name,
    description="A beginner-friendly FastAPI wrapper around a local or remote Ollama model.",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "message": "Welcome to the Deployable AI Agent API.",
        "docs": "/docs",
        "health": "/health",
        "chat": "/chat",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        ollama_base_url=settings.ollama_base_url,
        model=settings.ollama_model,
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    selected_model = request.model or settings.ollama_model

    try:
        answer = await ask_ollama(
            message=request.message,
            system_prompt=request.system_prompt,
            model=selected_model,
        )
    except OllamaError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(response=answer, model=selected_model)
