from datetime import datetime
from app.config.settings import CLASS_NAMES


class ReportAgent:
    """
    Generates text-based diagnostic reports
    """

    def generate_report(self, prediction, explanation):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
BRAIN MRI CLASSIFICATION REPORT
Generated: {timestamp}

Diagnosis: {prediction['predicted_class'].upper()}
Confidence: {prediction['confidence']:.2f}%

Explanation:
{explanation}

Classes:
{', '.join(CLASS_NAMES)}
"""
        return report
