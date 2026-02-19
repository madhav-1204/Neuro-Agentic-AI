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

    # ── Shared helpers ──────────────────────────────────────────────

    def _create_pdf(self, title):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        # PDF metadata (#22)
        pdf.set_title(title)
        pdf.set_author("Neuro Agentic AI")
        pdf.set_creator("Neuro Agentic AI v2.0")
        pdf.set_subject("Brain MRI AI Analysis Report")
        pdf.set_creation_date(datetime.now())
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

    def _safe(self, text):
        """Sanitise text for FPDF (replace unsupported chars)."""
        if not text:
            return "N/A"
        return (
            text.replace("\u2013", "-")
            .replace("\u2014", "--")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2022", "-")
            .replace("\u2026", "...")
            .encode("latin-1", "replace")
            .decode("latin-1")
        )

    # ── Classic single-scan PDF ─────────────────────────────────────

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

    # ── 3-page Claude analysis report ──────────────────────────────

    def generate_claude_report(self, result, filename=None):
        """
        3-page PDF generated from the Claude vision analysis response.

        Page 1: Header / Disclaimer / Detection Results / What / Why / Symptoms
        Page 2: Treatment / Prognosis / GradCAM Technical Details
        Page 3: Full Medical & Legal Disclaimers
        """
        analysis = result.get("analysis", {})
        scan_name = result.get("filename", "unknown_scan")
        patient_name = result.get("patientName", "Unknown Patient")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        # PDF metadata (#22)
        pdf.set_title(f"Brain MRI Report - {patient_name}")
        pdf.set_author("Neuro Agentic AI")
        pdf.set_creator("Neuro Agentic AI v2.0")
        pdf.set_subject("Brain Tumor Detection Report")
        pdf.set_creation_date(datetime.now())

        # ── PAGE 1 ──────────────────────────────────────────────────
        pdf.add_page()

        # Header
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 12, "Neuro Agentic AI", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Brain Tumor Detection Report", ln=True, align="C")
        pdf.cell(0, 5, f"Generated: {now_str}", ln=True, align="C")
        pdf.ln(4)

        # Disclaimer banner
        pdf.set_fill_color(255, 240, 240)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(
            0, 7,
            "DISCLAIMER: AI-generated analysis. Not a substitute for professional medical diagnosis.",
            ln=True, align="C", fill=True,
        )
        pdf.ln(6)

        # Scan info
        self._section(
            pdf, "Patient Information",
            f"Patient Name: {self._safe(patient_name)}\nFile: {scan_name}",
        )

        # Detection results
        tumor_type = self._safe(analysis.get("tumorType", "N/A"))
        confidence = self._safe(analysis.get("confidence", "N/A"))
        region = self._safe(analysis.get("region", "N/A"))
        grade = self._safe(analysis.get("grade", "N/A"))

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, "Detection Results", ln=True)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(
            0, 6,
            f"Tumor Type:   {tumor_type}\n"
            f"Confidence:   {confidence}\n"
            f"Region:       {region}\n"
            f"WHO Grade:    {grade}",
        )
        pdf.ln(4)

        # What is it?
        self._section(
            pdf,
            "What Is This Tumor?",
            self._safe(analysis.get("whatIsIt", "N/A")),
        )

        # Why it occurred
        self._section(
            pdf,
            "Why It May Have Occurred",
            self._safe(analysis.get("whyItOccurred", "N/A")),
        )

        # Symptoms
        self._section(
            pdf,
            "Typical Symptoms",
            self._safe(analysis.get("symptoms", "N/A")),
        )

        # ── PAGE 2 ──────────────────────────────────────────────────
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 12, "Treatment & Prognosis", ln=True, align="C")
        pdf.ln(6)

        # Treatment protocols
        self._section(
            pdf,
            "Standard Treatment Protocols",
            self._safe(analysis.get("treatment", "N/A")),
        )

        # Prognosis
        self._section(
            pdf,
            "Prognosis & Survival Statistics",
            self._safe(analysis.get("prognosis", "N/A")),
        )

        # GradCAM technical overview
        regions = analysis.get("gradcamRegions", [])
        if regions:
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 9, "GradCAM Activation Regions", ln=True)
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(35, 7, "Region #", border=1, align="C")
            pdf.cell(30, 7, "X", border=1, align="C")
            pdf.cell(30, 7, "Y", border=1, align="C")
            pdf.cell(30, 7, "W", border=1, align="C")
            pdf.cell(30, 7, "H", border=1, align="C")
            pdf.cell(35, 7, "Intensity", border=1, align="C")
            pdf.ln()

            for idx, r in enumerate(regions, 1):
                pdf.cell(35, 7, str(idx), border=1, align="C")
                pdf.cell(30, 7, f"{r.get('x', 0):.3f}", border=1, align="C")
                pdf.cell(30, 7, f"{r.get('y', 0):.3f}", border=1, align="C")
                pdf.cell(30, 7, f"{r.get('w', 0):.3f}", border=1, align="C")
                pdf.cell(30, 7, f"{r.get('h', 0):.3f}", border=1, align="C")
                pdf.cell(35, 7, f"{r.get('intensity', 0):.2f}", border=1, align="C")
                pdf.ln()

            pdf.ln(4)
            pdf.set_font("Helvetica", "I", 9)
            pdf.multi_cell(
                0, 5,
                "GradCAM (Gradient-weighted Class Activation Mapping) highlights "
                "regions of the image that most strongly influenced the AI's prediction. "
                "Higher intensity values correspond to areas more critical for the diagnosis.",
            )
        pdf.ln(4)

        # ── PAGE 3 ──────────────────────────────────────────────────
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "Important Disclaimers", ln=True, align="C")
        pdf.ln(6)

        disclaimers = [
            (
                "Medical Disclaimer",
                "This report is generated by an artificial intelligence system and is "
                "intended for informational and educational purposes only. It does NOT "
                "constitute a medical diagnosis, professional medical advice, or "
                "treatment recommendation. All findings should be reviewed and validated "
                "by a qualified healthcare professional. AI predictions may contain "
                "errors and should never be used as the sole basis for clinical decisions.",
            ),
            (
                "Accuracy Limitations",
                "The AI model's predictions are based on patterns learned from training "
                "data and may not generalize to all cases. Factors such as image quality, "
                "scan orientation, patient demographics, and rare tumor variants may "
                "affect accuracy. Confidence scores reflect model certainty, not medical "
                "certainty.",
            ),
            (
                "Privacy Notice",
                "Uploaded images are processed in memory and are not stored permanently. "
                "However, users should ensure they have proper authorization before "
                "uploading any medical imagery. This system is not certified under HIPAA, "
                "GDPR, or other healthcare data protection regulations for clinical use.",
            ),
            (
                "Emergency Contact Information",
                "If you or a patient is experiencing a medical emergency, contact "
                "emergency services immediately:\n"
                "- Emergency (US): 911\n"
                "- Poison Control (US): 1-800-222-1222\n"
                "- National Cancer Institute: 1-800-4-CANCER (1-800-422-6237)\n"
                "- Brain Tumor Foundation: 1-212-265-2401",
            ),
        ]

        for title, body in disclaimers:
            self._section(pdf, title, self._safe(body))

        # Footer
        pdf.ln(6)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(
            0, 5,
            f"Report generated by Neuro Agentic AI on {now_str}. "
            "Powered by Gemini Vision AI.",
            ln=True, align="C",
        )

        out_name = (
            filename
            or f"claude_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        out_path = os.path.join(self.output_dir, out_name)
        pdf.output(out_path)
        return out_path

    # ── Batch report (unchanged) ────────────────────────────────────

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
