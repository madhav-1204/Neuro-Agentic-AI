"""
Generate Software Requirements Specification PDF for Neuro Diagnosis AI
"""
from fpdf import FPDF
from datetime import datetime


class SRSPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Neuro Diagnosis AI - Software Requirements Specification", align="R")
        self.ln(4)
        self.set_draw_color(0, 71, 161)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 71, 161)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 71, 161)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(4)

    def sub_section(self, num, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, f"{num} {title}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def add_table(self, headers, data, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 71, 161)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in data:
            if self.get_y() > 260:
                self.add_page()
            if fill:
                self.set_fill_color(235, 242, 250)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 7
            # Calculate max height needed
            for i, cell in enumerate(row):
                lines = self.multi_cell(col_widths[i], 5.5, str(cell), split_only=True)
                h = len(lines) * 5.5
                if h > max_h:
                    max_h = h
            x_start = self.get_x()
            y_start = self.get_y()
            for i, cell in enumerate(row):
                self.set_xy(x_start + sum(col_widths[:i]), y_start)
                self.multi_cell(col_widths[i], max_h / max(1, len(self.multi_cell(col_widths[i], 5.5, str(cell), split_only=True))),
                                str(cell), border=1, fill=True)
            self.set_xy(x_start, y_start + max_h)
            fill = not fill
        self.ln(4)

    def add_simple_table(self, headers, data, col_widths=None):
        """Simple single-line-per-row table."""
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 71, 161)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in data:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(235, 242, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(4)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)


def generate():
    pdf = SRSPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Cover Page ─────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 71, 161)
    pdf.cell(0, 15, "SOFTWARE REQUIREMENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, "SPECIFICATION", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(0, 71, 161)
    pdf.set_line_width(1)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, "Neuro Diagnosis AI", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "AI-Powered Brain Tumor Classification & Explainability System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    info = [
        ("Institution", "CMR Technical Campus (UGC Autonomous)"),
        ("Department", "Computer Science and Engineering"),
        ("Batch", "A6"),
        ("Team", "K. Sai Sri Madhav, Arvind Reddy, Ashritha"),
        ("Guide", "Dr. Narshima Rao"),
        ("Date", datetime.now().strftime("%B %d, %Y")),
        ("Version", "2.0.0"),
    ]
    for label, value in info:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(45, 7, f"{label}:", align="R")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, f"  {value}", new_x="LMARGIN", new_y="NEXT")

    # ── 1. Introduction ────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("1", "Introduction")

    pdf.sub_section("1.1", "Purpose")
    pdf.body_text(
        "Neuro Diagnosis AI is an AI-powered web-based system that automates brain MRI classification "
        "into four categories - Glioma, Meningioma, Pituitary Tumor, and No Tumor - using deep learning "
        "models. The system provides visual explainability through Grad-CAM heatmaps and AI-generated "
        "medical explanations via Google Gemini."
    )

    pdf.sub_section("1.2", "Scope")
    pdf.body_text(
        "The system serves as a diagnostic aid for healthcare professionals, providing rapid MRI scan "
        "analysis with transparent, explainable results. It supports single-scan analysis, multi-scan "
        "analysis for a single patient, and batch multi-patient processing for diagnostic centers."
    )

    pdf.sub_section("1.3", "Project Team")
    pdf.add_simple_table(
        ["Role", "Name", "ID"],
        [
            ["Team Member", "K. Sai Sri Madhav", "247R1A0525"],
            ["Team Member", "Arvind Reddy", "257R5A0504"],
            ["Team Member", "Ashritha", "247R1A0525"],
            ["Project Guide", "Dr. Narshima Rao", "Faculty Supervisor"],
        ],
        [50, 80, 60],
    )

    # ── 2. Hardware Requirements ────────────────────────────────
    pdf.section_title("2", "Hardware Requirements")
    pdf.add_simple_table(
        ["Component", "Minimum", "Recommended"],
        [
            ["Processor", "Intel i5 / AMD Ryzen 5", "Intel i7 / AMD Ryzen 7+"],
            ["RAM", "8 GB", "16 GB"],
            ["Storage", "5 GB free disk space", "10 GB SSD"],
            ["GPU", "Not required (CPU supported)", "NVIDIA GPU with CUDA"],
            ["Network", "Internet connection", "Broadband connection"],
        ],
        [45, 72, 73],
    )

    # ── 3. Software Requirements ────────────────────────────────
    pdf.section_title("3", "Software Requirements")

    pdf.sub_section("3.1", "Operating System")
    pdf.add_simple_table(
        ["OS", "Version"],
        [
            ["Windows", "10 / 11"],
            ["Linux", "Ubuntu 20.04+ / any modern distro"],
            ["macOS", "12 Monterey+"],
        ],
        [60, 130],
    )

    pdf.sub_section("3.2", "Runtime Environments")
    pdf.add_simple_table(
        ["Software", "Version", "Purpose"],
        [
            ["Python", "3.11+", "Backend runtime"],
            ["Node.js", "20+", "Frontend runtime"],
            ["npm", "9+", "Package manager"],
            ["pip", "21+", "Python package manager"],
            ["Git", "2.30+", "Version control"],
        ],
        [40, 40, 110],
    )

    pdf.sub_section("3.3", "Backend Dependencies (Python)")
    pdf.add_simple_table(
        ["Category", "Package", "Version", "Purpose"],
        [
            ["Deep Learning", "torch", ">= 2.0.0", "Neural network framework"],
            ["Deep Learning", "torchvision", ">= 0.15.0", "Pre-trained models"],
            ["Deep Learning", "numpy", ">= 1.23.0", "Numerical computation"],
            ["Deep Learning", "pillow", ">= 10.0.0", "Image processing"],
            ["Deep Learning", "opencv-python-headless", ">= 4.9.0", "Image operations"],
            ["Explainability", "grad-cam", ">= 1.5.0", "Grad-CAM heatmaps"],
            ["Visualization", "matplotlib", ">= 3.8.0", "Visualization utilities"],
            ["LLM / AI", "google-genai", ">= 1.0.0", "Google Gemini API client"],
            ["Web Framework", "fastapi", "0.110.0", "REST API framework"],
            ["Web Framework", "uvicorn", "0.29.0", "ASGI server"],
            ["Web Framework", "python-multipart", "0.0.9", "File upload handling"],
            ["Web Framework", "slowapi", ">= 0.1.9", "API rate limiting"],
            ["Utilities", "requests", ">= 2.31.0", "HTTP client"],
            ["Utilities", "python-dotenv", ">= 1.0.0", "Env var management"],
            ["PDF", "fpdf2", ">= 2.8.5", "PDF report generation"],
            ["Testing", "pytest", ">= 7.0.0", "Unit testing"],
            ["Testing", "pytest-asyncio", ">= 0.23.0", "Async test support"],
            ["Testing", "httpx", ">= 0.27.0", "API testing"],
        ],
        [30, 50, 35, 75],
    )

    pdf.sub_section("3.4", "Frontend Dependencies (Node.js)")
    pdf.add_simple_table(
        ["Category", "Package", "Version", "Purpose"],
        [
            ["UI Framework", "react", "^19.2.0", "Component-based UI"],
            ["UI Framework", "react-dom", "^19.2.0", "DOM rendering"],
            ["Routing", "react-router-dom", "^7.13.0", "Client-side routing"],
            ["Animation", "gsap", "^3.14.2", "UI animations"],
            ["Build Tool", "vite", "^7.3.1", "Build and dev server"],
            ["Build Tool", "@vitejs/plugin-react", "^5.1.1", "React support for Vite"],
            ["Testing", "vitest", "^3.2.1", "Unit testing"],
            ["Testing", "@testing-library/react", "^16.3.0", "Component testing"],
            ["Testing", "@testing-library/jest-dom", "^6.6.3", "DOM matchers"],
            ["Testing", "jsdom", "^25.0.1", "DOM simulation"],
            ["Linting", "eslint", "^9.39.1", "Code quality"],
        ],
        [30, 55, 35, 70],
    )

    pdf.sub_section("3.5", "External APIs & Services")
    pdf.add_simple_table(
        ["Service", "Details"],
        [
            ["Google Gemini API", "Model: gemini-2.5-flash (configurable). AI-powered reasoning & vision analysis. Requires API key."],
        ],
        [50, 140],
    )

    pdf.sub_section("3.6", "Pre-trained Model Files")
    pdf.add_simple_table(
        ["File", "Architecture", "Location"],
        [
            ["brain_tumor_resnet18.pth", "ResNet-18", "backend/models/"],
            ["brain_tumor_efficientnet_b3.pth", "EfficientNet-B3", "backend/models/"],
        ],
        [70, 55, 65],
    )

    pdf.sub_section("3.7", "Database")
    pdf.add_simple_table(
        ["Component", "Details"],
        [
            ["Engine", "SQLite 3 (built into Python)"],
            ["File", "backend/neuro_ai.db (auto-created)"],
            ["Purpose", "Analysis audit trail / patient history"],
        ],
        [50, 140],
    )

    pdf.sub_section("3.8", "Optional - Docker Deployment")
    pdf.add_simple_table(
        ["Tool", "Version", "Purpose"],
        [
            ["Docker", "20+", "Containerization"],
            ["Docker Compose", "v2+", "Multi-container orchestration"],
            ["nginx", "Alpine", "Frontend static file serving"],
        ],
        [50, 40, 100],
    )

    # ── 4. Environment Configuration ────────────────────────────
    pdf.section_title("4", "Environment Configuration")
    pdf.add_simple_table(
        ["Variable", "Required", "Default", "Description"],
        [
            ["GEMINI_API_KEY", "Yes", "-", "Google Gemini API key"],
            ["GEMINI_MODEL", "No", "gemini-2.5-flash", "Gemini model name"],
            ["MODEL_ARCHITECTURE", "No", "resnet18", "resnet18 or efficientnet_b3"],
            ["MAX_UPLOAD_SIZE_MB", "No", "10", "Max upload size (MB)"],
            ["CORS_ORIGINS", "No", "-", "Extra CORS origins"],
            ["VITE_API_URL", "No", "http://127.0.0.1:8000", "Backend URL for frontend"],
        ],
        [42, 20, 48, 80],
    )

    # ── 5. Functional Requirements ──────────────────────────────
    pdf.section_title("5", "Functional Requirements")
    pdf.add_simple_table(
        ["ID", "Module", "Requirement"],
        [
            ["FR-01", "Upload", "Accept MRI images in JPEG, PNG, WebP (max 10 MB)"],
            ["FR-02", "Classification", "Classify into Glioma, Meningioma, Pituitary, No Tumor"],
            ["FR-03", "Confidence", "Provide per-class probability scores with confidence"],
            ["FR-04", "Explainability", "Generate Grad-CAM heatmap overlays"],
            ["FR-05", "Reasoning", "Generate AI-powered medical explanations"],
            ["FR-06", "Vision Analysis", "Support direct Gemini Vision analysis"],
            ["FR-07", "PDF Reports", "Generate downloadable PDF diagnostic reports"],
            ["FR-08", "Single Analysis", "Single MRI scan analysis with patient name"],
            ["FR-09", "Multi-Scan", "Multiple MRI scans for one patient"],
            ["FR-10", "Batch Processing", "Multi-patient batch analysis"],
            ["FR-11", "Audit Trail", "Log all analyses to SQLite with timestamps"],
            ["FR-12", "History", "API endpoint to retrieve analysis history"],
            ["FR-13", "Health Check", "Expose /health endpoint for monitoring"],
        ],
        [17, 30, 143],
    )

    # ── 6. Non-Functional Requirements ──────────────────────────
    pdf.section_title("6", "Non-Functional Requirements")
    pdf.add_simple_table(
        ["ID", "Category", "Requirement"],
        [
            ["NFR-01", "Performance", "Handle up to 60 requests/min per client"],
            ["NFR-02", "Scalability", "Docker deployment for horizontal scaling"],
            ["NFR-03", "Reliability", "Retry up to 4 times with exponential backoff"],
            ["NFR-04", "Fallback", "Static fallback when Gemini API unavailable"],
            ["NFR-05", "Security", "CORS restricted to configured origins"],
            ["NFR-06", "Privacy", "Uploaded files deleted after analysis"],
            ["NFR-07", "Compliance", "Medical disclaimer on all reports"],
            ["NFR-08", "Usability", "Animated transitions & real-time progress"],
            ["NFR-09", "Error Handling", "Global exception handler with structured errors"],
        ],
        [17, 30, 143],
    )

    # ── 7. System Architecture ──────────────────────────────────
    pdf.section_title("7", "System Architecture")
    pdf.body_text(
        "The system follows a multi-agent architecture where an Orchestrator coordinates four "
        "specialized agents in a sequential pipeline:"
    )
    pdf.ln(2)

    agents = [
        ("Vision Agent", "Deep learning CNN (ResNet-18 / EfficientNet-B3) for MRI classification with per-class probability scores."),
        ("Explainability Agent", "Grad-CAM heatmap generation over the final convolutional layer, providing visual transparency."),
        ("Reasoning Agent", "Google Gemini LLM that generates medical explanations covering diagnosis, symptoms, treatment, and prognosis."),
        ("Report Agent", "Compiles prediction, explanation, and metadata into structured text and downloadable PDF reports."),
    ]
    for name, desc in agents:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 71, 161)
        pdf.cell(6, 5.5, "-")
        pdf.cell(45, 5.5, name + ":")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5.5, desc)
        pdf.ln(2)

    pdf.ln(2)
    pdf.body_text("Additionally, the Gemini Vision Agent provides direct image analysis as an alternative pipeline, "
                  "sending the MRI directly to Gemini's vision API for structured tumor analysis with simulated GradCAM regions.")

    pdf.body_text(
        "Architecture Flow:  MRI Upload -> Vision Agent -> Explainability Agent -> Reasoning Agent -> Report Agent"
    )

    # ── 8. API Endpoints ────────────────────────────────────────
    pdf.section_title("8", "API Endpoints")
    pdf.add_simple_table(
        ["Method", "Endpoint", "Description"],
        [
            ["GET", "/", "Server status"],
            ["GET", "/health", "Health check"],
            ["POST", "/analyze", "Single MRI analysis (CNN + Grad-CAM + Gemini)"],
            ["POST", "/analyze/batch", "Batch MRI analysis (multiple files)"],
            ["POST", "/analyze/gemini", "Single MRI via Gemini Vision"],
            ["POST", "/analyze/gemini/batch", "Batch MRI via Gemini Vision"],
            ["POST", "/analyze/gemini/download-pdf", "Download PDF (Gemini analysis)"],
            ["POST", "/analyze/download-pdf", "Download PDF (standard analysis)"],
            ["GET", "/analyze/history", "Retrieve analysis audit trail"],
        ],
        [18, 62, 110],
    )

    # ── 9. Supported File Formats ──────────────────────────────
    pdf.section_title("9", "Supported File Formats")
    pdf.add_simple_table(
        ["Format", "Extension", "MIME Type"],
        [
            ["JPEG", ".jpg, .jpeg", "image/jpeg"],
            ["PNG", ".png", "image/png"],
            ["WebP", ".webp", "image/webp"],
        ],
        [40, 60, 90],
    )
    pdf.body_text("Maximum file size: 10 MB (configurable via MAX_UPLOAD_SIZE_MB)")

    # ── 10. Network Ports ──────────────────────────────────────
    pdf.section_title("10", "Network Ports")
    pdf.add_simple_table(
        ["Service", "Port", "Protocol"],
        [
            ["Backend (FastAPI / Uvicorn)", "8000", "HTTP"],
            ["Frontend (Vite dev server)", "5173", "HTTP"],
            ["Frontend (Docker / nginx)", "80", "HTTP"],
        ],
        [80, 40, 70],
    )

    # ── 11. Validation ─────────────────────────────────────────
    pdf.section_title("11", "Validation")
    pdf.add_simple_table(
        ["Type", "Validation Rule", "Outcome"],
        [
            ["Input Validation", "Accept only JPEG, PNG, WebP and reject unsupported extensions", "Prevents invalid file processing"],
            ["Size Validation", "Reject uploads above MAX_UPLOAD_SIZE_MB (default: 10 MB)", "Protects service from oversized payloads"],
            ["Schema Validation", "Validate API request fields and mandatory parameters", "Ensures consistent request contracts"],
            ["Inference Validation", "Check model output probabilities sum to 1.0", "Improves prediction consistency"],
            ["Report Validation", "Verify PDF sections and mandatory disclaimer before export", "Guarantees report completeness"],
            ["Error Validation", "Return structured error responses with status code and details", "Improves debugging and client handling"],
        ],
        [42, 90, 58],
    )

    # ── 12. Uploading Dataset ──────────────────────────────────
    pdf.section_title("12", "Uploading Dataset")
    pdf.body_text(
        "The platform supports dataset uploads for batch analysis workflows and future model retraining pipelines. "
        "Dataset ingestion must preserve data integrity, privacy, and traceability."
    )
    pdf.add_simple_table(
        ["Step", "Description"],
        [
            ["1. Dataset Packaging", "Organize MRI files by class labels and include metadata (patient ID, modality, scan date where available)."],
            ["2. Upload Interface", "Use secure multipart upload endpoints or admin upload panel for ZIP/folder ingestion."],
            ["3. Automatic Checks", "Validate file formats, naming conventions, duplicate detection, and corrupted image filtering."],
            ["4. Storage & Indexing", "Store accepted files in managed storage and index references in the analysis database."],
            ["5. Audit Logging", "Track uploader, timestamp, dataset version, and validation status for compliance."],
        ],
        [45, 145],
    )

    # ── 13. Future Aspects ─────────────────────────────────────
    pdf.section_title("13", "Future Aspects")
    future_aspects = [
        "Federated learning support for privacy-preserving multi-hospital training.",
        "DICOM native ingestion with metadata-aware preprocessing and anonymization.",
        "Model drift monitoring dashboard with automatic revalidation alerts.",
        "Role-based clinical workflows with approval checkpoints and e-signatures.",
        "FHIR/HL7 interoperability for direct hospital information system integration.",
        "Expanded pathology coverage beyond tumors, such as stroke and hemorrhage triage.",
    ]
    for aspect in future_aspects:
        pdf.bullet(aspect)

    # ── 14. References ─────────────────────────────────────────
    pdf.section_title("14", "References")
    references = [
        "He, K., Zhang, X., Ren, S., and Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR.",
        "Tan, M., and Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. ICML.",
        "Selvaraju, R.R., et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. ICCV.",
        "FastAPI documentation: https://fastapi.tiangolo.com/",
        "PyTorch documentation: https://pytorch.org/docs/stable/",
        "Google Gemini API documentation: https://ai.google.dev/gemini-api/docs",
        "FPDF2 documentation: https://py-pdf.github.io/fpdf2/",
    ]
    for ref in references:
        pdf.bullet(ref)

    # ── Save ────────────────────────────────────────────────────
    output_path = "Neuro_Diagnosis_AI_SRS_Updated.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate()
