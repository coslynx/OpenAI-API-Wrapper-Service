from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

from api.dependencies import openai_service
from api.models import openai_models
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/openai",
    tags=["OpenAI"],
)

@router.post("/generate_response")
async def generate_response(
    request: Request,
    openai_service_instance: openai_service.OpenAIService = Depends(openai_service.get_openai_service)
):
    """
    Generates an AI response using the OpenAI API.

    Args:
        request:  FastAPI request object containing the user's prompt.
        openai_service_instance:  Instance of the `OpenAIService` for interacting with OpenAI.

    Returns:
        JSONResponse:  A JSON response containing the generated AI response.

    Raises:
        HTTPException:  Raises an HTTPException with appropriate error codes and messages for various scenarios.
    """
    try:
        request_data = await request.json()
        prompt = openai_models.PromptRequest(**request_data)
        response = await openai_service_instance.generate_response(prompt)
        return JSONResponse({"response": response})

    except openai_models.ValidationError as e:
        logger.error(f"Invalid request data: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request data: {e}")

    except openai_service.OpenAIServiceError as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")

    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")