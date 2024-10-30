from pydantic import BaseModel, validator
from typing import Optional

class PromptRequest(BaseModel):
    model: str = "text-davinci-003"  # Default OpenAI model
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[list[str]] = None

    @validator("prompt")
    def prompt_cannot_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Prompt cannot be empty.")
        return value

    @validator("max_tokens")
    def max_tokens_valid(cls, value):
        if value <= 0:
            raise ValueError("Max tokens must be greater than 0.")
        return value

    @validator("temperature")
    def temperature_valid(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Temperature must be between 0 and 1.")
        return value

    @validator("top_p")
    def top_p_valid(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Top P must be between 0 and 1.")
        return value

    @validator("frequency_penalty")
    def frequency_penalty_valid(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Frequency penalty must be between 0 and 1.")
        return value

    @validator("presence_penalty")
    def presence_penalty_valid(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Presence penalty must be between 0 and 1.")
        return value

class OpenAIResponse(BaseModel):
    response: str
    model: str
    usage: dict

class ValidationError(Exception):
    """Custom exception for invalid request data."""
    pass