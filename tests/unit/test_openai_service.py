import unittest
from unittest.mock import patch, MagicMock
from typing import Optional

from api.dependencies import openai_service
from api.models import openai_models
from config.settings import settings
from utils.exceptions import OpenAIServiceError

class TestOpenAIService(unittest.TestCase):
    """Test suite for the OpenAIService class."""

    @patch("openai.OpenAI")
    def test_init(self, mock_openai):
        """Test initialization of the OpenAIService class."""
        api_key = "test_api_key"
        openai_service_instance = openai_service.OpenAIService(api_key)
        self.assertEqual(openai_service_instance.openai, mock_openai.return_value)
        self.assertEqual(openai_service_instance.cache, {})
        self.assertEqual(openai_service_instance.rate_limit, 5)
        self.assertEqual(openai_service_instance.last_call, 0)

    @patch("openai.OpenAI.completions.create")
    def test_generate_response_success(self, mock_create):
        """Test successful generation of a response using OpenAI API."""
        prompt = "Test prompt"
        model = "text-davinci-003"
        expected_response = "Test response"
        mock_create.return_value = MagicMock(choices=[MagicMock(text=expected_response)])
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        response = openai_service_instance.generate_response(prompt, model)
        self.assertEqual(response, expected_response)
        mock_create.assert_called_once_with(
            model=model, prompt=prompt, max_tokens=100, temperature=0.7
        )

    @patch("openai.OpenAI.completions.create")
    def test_generate_response_error(self, mock_create):
        """Test error handling during API call."""
        mock_create.side_effect = Exception("Error calling OpenAI API")
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        with self.assertRaisesRegex(
            OpenAIServiceError, "Error calling OpenAI API: Error calling OpenAI API"
        ):
            openai_service_instance.generate_response("Test prompt")

    def test_check_rate_limit(self):
        """Test rate limiting functionality."""
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        openai_service_instance.last_call = 0
        openai_service_instance._check_rate_limit()
        self.assertGreater(openai_service_instance.last_call, 0)

    @patch("openai.OpenAI.completions.create")
    def test_generate_response_caching(self, mock_create):
        """Test caching of API responses."""
        prompt = "Test prompt"
        model = "text-davinci-003"
        expected_response = "Test response"
        mock_create.return_value = MagicMock(choices=[MagicMock(text=expected_response)])
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        response1 = openai_service_instance.generate_response(prompt, model)
        self.assertEqual(response1, expected_response)
        mock_create.assert_called_once()
        response2 = openai_service_instance.generate_response(prompt, model)
        self.assertEqual(response2, expected_response)
        mock_create.assert_called_once()

    @patch("api.dependencies.openai_service.OpenAIService.generate_response")
    def test_get_openai_service(self, mock_generate_response):
        """Test dependency injection of OpenAIService instance."""
        api_key = "test_api_key"
        settings.OPENAI_API_KEY = api_key
        openai_service_instance = openai_service.get_openai_service()
        self.assertIsInstance(openai_service_instance, openai_service.OpenAIService)
        self.assertEqual(openai_service_instance.openai.api_key, api_key)

    @patch("openai.OpenAI.completions.create")
    def test_generate_response_with_prompt_request(self, mock_create):
        """Test handling a PromptRequest object."""
        prompt_request = openai_models.PromptRequest(prompt="Test prompt", model="text-davinci-003")
        expected_response = "Test response"
        mock_create.return_value = MagicMock(choices=[MagicMock(text=expected_response)])
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        response = openai_service_instance.generate_response(prompt_request.prompt, prompt_request.model)
        self.assertEqual(response, expected_response)
        mock_create.assert_called_once_with(
            model=prompt_request.model,
            prompt=prompt_request.prompt,
            max_tokens=prompt_request.max_tokens,
            temperature=prompt_request.temperature,
            top_p=prompt_request.top_p,
            frequency_penalty=prompt_request.frequency_penalty,
            presence_penalty=prompt_request.presence_penalty,
            stop=prompt_request.stop,
        )

    def test_generate_response_invalid_model(self):
        """Test handling an invalid OpenAI model."""
        openai_service_instance = openai_service.OpenAIService("test_api_key")
        with self.assertRaisesRegex(
            OpenAIServiceError, "Invalid OpenAI model: invalid_model"
        ):
            openai_service_instance.generate_response("Test prompt", model="invalid_model")