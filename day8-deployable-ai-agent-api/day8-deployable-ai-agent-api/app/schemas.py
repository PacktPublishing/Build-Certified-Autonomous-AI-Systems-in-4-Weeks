from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_name: str
    ollama_base_url: str
    model: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user's message for the agent.")
    system_prompt: str | None = Field(
        default="You are a helpful AI assistant. Keep answers clear and beginner-friendly.",
        description="Optional instruction that controls how the model should behave.",
    )
    model: str | None = Field(
        default=None,
        description="Optional Ollama model override. If empty, the app default is used.",
    )


class ChatResponse(BaseModel):
    response: str
    model: str
