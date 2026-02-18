import os
import json
import re
import time
import logging

from app.config.settings import GEMINI_MODEL

logger = logging.getLogger(__name__)

try:
    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


SYSTEM_PROMPT = (
    "You are an expert neuroradiologist AI. Analyze the provided brain MRI/CT image "
    "and return ONLY a valid JSON object. Do not include markdown, backticks, or any "
    "extra text. Return exactly this JSON structure:\n"
    "{\n"
    '  "tumorType": "string — tumor name (e.g. Glioblastoma Multiforme, Meningioma, '
    'Medulloblastoma, Pituitary Adenoma, etc.)",\n'
    '  "confidence": "string — confidence level (e.g. High ~87%)",\n'
    '  "region": "string — brain region (e.g. Right Temporal Lobe)",\n'
    '  "grade": "string — WHO grade if applicable (e.g. Grade IV)",\n'
    '  "whatIsIt": "string — 3-4 sentence explanation of this tumor type: what it is, '
    'cellular origin, typical presentation",\n'
    '  "whyItOccurred": "string — 3-4 sentences explaining known risk factors, genetic '
    'mutations, environmental triggers, or idiopathic nature",\n'
    '  "symptoms": "string — 3-4 sentences describing typical clinical symptoms this '
    'tumor causes",\n'
    '  "treatment": "string — 3-4 sentences on standard treatment protocols (surgery, '
    'radiation, chemotherapy, immunotherapy)",\n'
    '  "prognosis": "string — 2-3 sentences on typical prognosis and survival '
    'statistics",\n'
    '  "gradcamRegions": [\n'
    '    { "x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0, "intensity": 0.0 }\n'
    "  ]\n"
    "}\n"
    "The gradcamRegions array should contain 4-8 objects representing activation "
    "hotspots. Values are normalized 0-1 relative to image dimensions. The "
    "highest-intensity region should correspond to the suspected tumor location. "
    "intensity ranges 0.1-1.0 where 1.0 is maximum activation."
)


class GeminiVisionAgent:
    """
    Sends brain MRI images to Gemini's vision API for analysis.
    Returns structured JSON with tumor info + GradCAM regions.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model = GEMINI_MODEL

        if self.api_key and GEMINI_AVAILABLE:
            self.client = genai.Client(api_key=self.api_key)

    @staticmethod
    def _read_image_bytes(image_path: str) -> tuple[bytes, str]:
        """Read image file and return (raw_bytes, mime_type)."""
        ext = os.path.splitext(image_path)[1].lower()
        media_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        mime_type = media_map.get(ext, "image/jpeg")

        with open(image_path, "rb") as f:
            data = f.read()

        return data, mime_type

    def analyze(self, image_path: str) -> dict:
        """
        Send image to Gemini and get structured tumor analysis back.
        """
        if not self.client:
            raise RuntimeError(
                "Gemini client not initialised. "
                "Set GEMINI_API_KEY in your .env file."
            )

        image_bytes, mime_type = self._read_image_bytes(image_path)

        prompt_text = (
            SYSTEM_PROMPT
            + "\n\nAnalyze this brain scan image for tumor detection "
            "and provide the full JSON response as instructed."
        )
        content = [
            types.Content(
                parts=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    types.Part.from_text(text=prompt_text),
                ]
            )
        ]

        # Retry with exponential backoff for 429 rate-limit errors
        models_to_try = [self.model, "gemini-2.5-flash-lite"]
        last_error = None

        for model_name in models_to_try:
            for attempt in range(4):  # up to 4 attempts per model
                try:
                    logger.info(f"Gemini request: model={model_name}, attempt={attempt+1}")
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=content,
                    )
                    raw = response.text.strip()
                    raw = re.sub(r"^```(?:json)?\s*", "", raw)
                    raw = re.sub(r"\s*```$", "", raw)

                    try:
                        return json.loads(raw)
                    except json.JSONDecodeError:
                        return {"error": "Failed to parse Gemini response", "raw": raw}

                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        wait = (2 ** attempt) * 2  # 2, 4, 8, 16 seconds
                        logger.warning(f"Rate limited (429). Waiting {wait}s before retry...")
                        time.sleep(wait)
                        continue
                    else:
                        raise  # Non-rate-limit error, re-raise immediately

            logger.warning(f"All retries exhausted for {model_name}, trying next model...")

        raise RuntimeError(f"All Gemini models exhausted after retries. Last error: {last_error}")
