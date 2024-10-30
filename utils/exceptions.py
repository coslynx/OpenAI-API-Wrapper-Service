class OpenAIServiceError(Exception):
    """Represents general OpenAI service errors."""

    def __init__(self, message: str, code: int = 500):
        """Initializes the exception with a message and an optional error code."""
        super().__init__(message)
        self.code = code

class InvalidPromptError(Exception):
    """Represents invalid prompt formatting."""

    def __init__(self, message: str, code: int = 400):
        """Initializes the exception with a message and an optional error code."""
        super().__init__(message)
        self.code = code

class OpenAIRequestError(Exception):
    """Represents errors during API requests."""

    def __init__(self, message: str, code: int = 500):
        """Initializes the exception with a message and an optional error code."""
        super().__init__(message)
        self.code = code

class OpenAIResponseError(Exception):
    """Represents errors during response processing."""

    def __init__(self, message: str, code: int = 500):
        """Initializes the exception with a message and an optional error code."""
        super().__init__(message)
        self.code = code