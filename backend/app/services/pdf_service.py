import os
from datetime import datetime
from fpdf import FPDF


class PDFService:
    """
    Generates PDF reports from inference results.
    Paths are anchored to the backend root directory.
    """

    def __init__(self, output_dir=None):
        # Resolve backend root dynamically
        backend_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        # backend/app/services -> backend/

        self.output_dir = output_dir or os.path.join(backend_root, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def _create_pdf(self, title):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(5)
        return pdf

    def _section(self, pdf, title, body):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, title, ln=True)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, body)
        pdf.ln(3)

    def generate_single_scan_pdf(self, result, filename=None):
        pdf = self._create_pdf("Brain MRI AI Report")

        prediction = result["prediction"]

        self._section(
            pdf,
            "Scan Information",
            f"Filename: {result['filename']}\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )

        self._section(
            pdf,
            "AI Prediction",
            f"Diagnosis: {prediction['predicted_class'].upper()}\n"
            f"Confidence: {prediction['confidence']:.2f}%",
        )

        probs_text = "\n".join(
            f"{cls}: {prob*100:.2f}%"
            for cls, prob in zip(
                prediction["class_names"],
                prediction["probabilities"],
            )
        )

        self._section(pdf, "Probability Distribution", probs_text)

        self._section(
            pdf,
            "Explanation",
            result.get("explanation", "No explanation available."),
        )

        out_name = (
            filename
            or f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        out_path = os.path.join(self.output_dir, out_name)
        pdf.output(out_path)

        return out_path

    def generate_batch_pdf(self, results, filename=None):
        pdf = self._create_pdf("Batch Brain MRI AI Report")

        self._section(
            pdf,
            "Batch Summary",
            f"Total scans analyzed: {len(results)}\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )

        for idx, result in enumerate(results, start=1):
            prediction = result["prediction"]

            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"Scan #{idx}: {result['filename']}", ln=True)
            pdf.ln(3)

            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(
                0,
                6,
                f"Diagnosis: {prediction['predicted_class'].upper()}\n"
                f"Confidence: {prediction['confidence']:.2f}%\n\n"
                f"Explanation:\n{result.get('explanation', 'N/A')}",
            )

        out_name = (
            filename
            or f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        out_path = os.path.join(self.output_dir, out_name)
        pdf.output(out_path)

        return out_path
