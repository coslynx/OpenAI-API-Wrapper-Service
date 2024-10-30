import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from typing import Optional

from api.routes import openai_routes
from api.dependencies import openai_service
from utils.logger import get_logger
from config.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(openai_routes.router)

logger = get_logger()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting the AI Interface for OpenAI Responses service.")
    openai_service.init_openai_service(settings.OPENAI_API_KEY)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the AI Interface for OpenAI Responses service.")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom exception handler for validation errors."""
    errors = exc.errors()
    logger.error(f"Validation error: {errors}")
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": errors}),
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Interface for OpenAI Responses service!"}