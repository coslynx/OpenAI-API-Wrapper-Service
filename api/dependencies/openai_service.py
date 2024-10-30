import os
from typing import Optional
from fastapi import Depends, HTTPException
from openai import OpenAI, Completion
from config.settings import settings
from utils.exceptions import OpenAIServiceError

class OpenAIServiceError(Exception):
    """Custom exception for OpenAI service errors."""
    pass

class OpenAIService:
    """Class for handling OpenAI API interactions."""

    def __init__(self, api_key: str):
        """Initializes the OpenAI service with the provided API key."""
        self.openai = OpenAI(api_key=api_key)
        self.cache = {}  # Simple in-memory cache for responses
        self.rate_limit = 5  # Example rate limit, adjust as needed
        self.last_call = 0

    async def generate_response(self, prompt: str, model: str = "text-davinci-003") -> str:
        """
        Generates an AI response using OpenAI's API.

        Args:
            prompt: The prompt to send to OpenAI.
            model: The OpenAI model to use for generating the response.

        Returns:
            str: The generated AI response.

        Raises:
            OpenAIServiceError: If an error occurs during the API call.
        """
        # Check rate limit
        self._check_rate_limit()

        # Check if response is cached
        cache_key = f"{prompt}_{model}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Construct the API request
            response = await self.openai.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=100,  # Example max tokens, adjust as needed
                temperature=0.7,  # Example temperature, adjust as needed
            )

            # Extract the generated response
            generated_response = response.choices[0].text

            # Cache the response
            self.cache[cache_key] = generated_response

            return generated_response

        except Exception as e:
            raise OpenAIServiceError(f"Error calling OpenAI API: {e}")

    def _check_rate_limit(self):
        """
        Enforces a rate limit to prevent exceeding API call limits.
        """
        import time

        # Example rate limiting implementation
        current_time = time.time()
        if current_time - self.last_call < self.rate_limit:
            time.sleep(self.rate_limit - (current_time - self.last_call))
        self.last_call = time.time()


# Create a dependency injection function to provide the OpenAI service
def get_openai_service(api_key: Optional[str] = Depends(settings.OPENAI_API_KEY)):
    """
    Dependency injection function to provide the OpenAIService instance.

    Args:
        api_key: The OpenAI API key.

    Returns:
        OpenAIService: The OpenAI service instance.
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="OpenAI API key is required.")

    return OpenAIService(api_key)