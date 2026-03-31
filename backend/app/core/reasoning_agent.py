import os
import logging
from app.config.settings import GEMINI_MODEL

logger = logging.getLogger(__name__)

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


REASONING_PROMPT = (
    "You are a neuroradiology AI assistant. Given the following brain MRI "
    "classification result, provide a concise 3-4 sentence medical explanation "
    "covering: (1) what the predicted condition means, (2) its clinical "
    "significance, and (3) recommended next steps. Be professional and factual.\n\n"
    "Predicted class: {predicted_class}\n"
    "Confidence: {confidence:.1f}%\n"
    "Class probabilities: {prob_summary}\n\n"
    "Respond with ONLY the explanation text, no headers or formatting."
)
class ReasoningAgent:
    """
    Generates medical explanations using Gemini (if available),
    with a static-string fallback when the API key is not set.
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

        try:
            prob_summary = ", ".join(
                f"{cls}: {prob*100:.1f}%"
                for cls, prob in zip(class_names, probabilities)
            )
            prompt = REASONING_PROMPT.format(
                predicted_class=predicted_class,
                confidence=confidence,
                prob_summary=prob_summary,
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=[types.Content(parts=[types.Part.from_text(text=prompt)])],
            )
            explanation = response.text.strip()
            if explanation:
                return explanation

            logger.warning("Empty Gemini response, using fallback.")
            return self._fallback(predicted_class, confidence)

        except Exception as e:
            logger.error("ReasoningAgent Gemini call failed: %s", e)
            return self._fallback(predicted_class, confidence)

    def _fallback(self, predicted_class, confidence):
        return (
            f"The model predicts {predicted_class} with {confidence:.1f}% confidence. "
            f"Please consult a qualified neuroradiologist for a definitive diagnosis. "
            f"This AI-generated result is for informational purposes only."
        )
