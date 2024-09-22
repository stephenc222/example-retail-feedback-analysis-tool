import google.generativeai as genai
import os
from src.utils.logging_utils import create_logger

DEFAULT_MODEL_NAME = "gemini-1.5-pro-001"


class LLMService:
    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        self.logger = create_logger(__name__)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, inputs):
        self.logger.info(
            f"Generating content with model: {self.model._model_name}")
        return self.model.generate_content(inputs)
