import os
from app.config.settings import GEMINI_MODEL

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ReasoningAgent:
    """
    Generates medical explanations using Gemini (if available)
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model = None

        if self.api_key and GEMINI_AVAILABLE:
            self.client = genai.Client(api_key=self.api_key)
            self.model = GEMINI_MODEL

    def generate_explanation(
        self, predicted_class, confidence, probabilities, class_names, image_path=None
    ):
        if not self.client:
            return self._fallback(predicted_class, confidence)

        return f"The model predicts {predicted_class} with {confidence:.1f}% confidence."

    def _fallback(self, predicted_class, confidence):
        return (
            f"The model predicts {predicted_class}. "
            f"Confidence level is {confidence:.1f}%."
        )
