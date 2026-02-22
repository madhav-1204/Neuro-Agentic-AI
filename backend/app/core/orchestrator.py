from app.core.vision_agent import VisionAgent
from app.core.explainability_agent import ExplainabilityAgent
from app.core.reasoning_agent import ReasoningAgent
from app.core.report_agent import ReportAgent
from app.core.gemini_vision_agent import GeminiVisionAgent  # noqa: F401


class Orchestrator:
    """
    Coordinates Vision → Explainability → Reasoning → Report
    """

    def __init__(self, gemini_api_key=None):
        self.vision_agent = VisionAgent()
        self.reasoning_agent = ReasoningAgent(api_key=gemini_api_key)
        self.report_agent = ReportAgent()
        self.explainability_agent = None

    def load_model(self):
        self.vision_agent.load_model()
        model = self.vision_agent.get_model_for_gradcam()
        self.explainability_agent = ExplainabilityAgent(model)

    def process_image(self, image_path):
        prediction = self.vision_agent.predict(image_path)

        gradcam = None
        if self.explainability_agent:
            gradcam = self.explainability_agent.explain(
                prediction["preprocessed_tensor"],
                prediction["original_image"],
                prediction["predicted_idx"],
            )

        explanation = self.reasoning_agent.generate_explanation(
            prediction["predicted_class"],
            prediction["confidence"],
            prediction["probabilities"],
            prediction["class_names"],
            image_path=image_path,
        )

        report = self.report_agent.generate_report(prediction, explanation)

        return {
            "prediction": prediction,
            "gradcam": gradcam,
            "explanation": explanation,
            "report": report,
        }
