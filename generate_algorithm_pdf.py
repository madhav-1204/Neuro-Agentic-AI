"""
Generate Algorithm Documentation PDF for Neuro Agentic AI
"""
from fpdf import FPDF
from datetime import datetime


class AlgorithmPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Neuro Agentic AI - Algorithm Documentation", align="R")
        self.ln(3)
        self.set_draw_color(0, 71, 161)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

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
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_section(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, lines):
        self.set_font("Courier", "", 8.5)
        self.set_text_color(30, 30, 30)
        self.set_fill_color(240, 240, 245)
        x = self.get_x()
        w = 190
        for line in lines:
            safe = line.encode("latin-1", "replace").decode("latin-1")
            if self.get_y() > 270:
                self.add_page()
            self.set_x(x)
            self.cell(w, 4.5, f"  {safe}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def arrow_line(self):
        cx = 105
        y = self.get_y()
        if y > 270:
            self.add_page()
            y = self.get_y()
        self.set_draw_color(0, 71, 161)
        self.set_line_width(0.4)
        self.line(cx, y, cx, y + 6)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 71, 161)
        self.set_xy(cx - 2, y + 3)
        self.cell(4, 4, "v", align="C")
        self.set_y(y + 8)

    def step_box(self, step_num, title, lines):
        self.set_draw_color(0, 71, 161)
        self.set_line_width(0.3)
        x0 = 15
        w = 180
        y_start = self.get_y()

        # Title bar
        self.set_fill_color(0, 71, 161)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.set_x(x0)
        self.cell(w, 6, f"  STEP {step_num}: {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

        # Content
        self.set_fill_color(245, 248, 255)
        self.set_font("Courier", "", 8)
        self.set_text_color(30, 30, 30)
        for line in lines:
            safe = line.encode("latin-1", "replace").decode("latin-1")
            if self.get_y() > 272:
                self.add_page()
            self.set_x(x0)
            self.cell(w, 4.2, f"  {safe}", fill=True, new_x="LMARGIN", new_y="NEXT")

        # Border
        y_end = self.get_y()
        self.rect(x0, y_start, w, y_end - y_start)
        self.ln(2)

    def table_row(self, cols, widths, bold=False, fill=False):
        self.set_font("Helvetica", "B" if bold else "", 8.5)
        if fill:
            self.set_fill_color(0, 71, 161)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(255, 255, 255)
            self.set_text_color(50, 50, 50)
        for i, (col, w) in enumerate(zip(cols, widths)):
            safe = str(col).encode("latin-1", "replace").decode("latin-1")
            self.cell(w, 6, safe, border=1, fill=fill or bold, align="C" if i > 0 else "L")
        self.ln()


def generate_pdf():
    pdf = AlgorithmPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── COVER PAGE ──
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(0, 71, 161)
    pdf.cell(0, 15, "Neuro Agentic AI", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Algorithm Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_draw_color(0, 71, 161)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "AI-Powered Brain MRI Analysis Platform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Multi-Agent Orchestration Pipeline", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Version 1.0", align="C", new_x="LMARGIN", new_y="NEXT")

    # ── TABLE OF CONTENTS ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(0, 71, 161)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    toc = [
        ("1", "System Overview Algorithm"),
        ("2", "Pipeline A - Local CNN Classification (Multi-Agent Orchestration)"),
        ("3", "Pipeline B - Gemini Vision Analysis (Multimodal LLM)"),
        ("4", "Classification Model Architecture"),
        ("5", "GradCAM Heatmap Algorithm"),
        ("6", "Batch & Multi-Patient Processing Algorithm"),
        ("7", "PDF Report Generation Algorithm"),
        ("8", "API Rate Limiting & Security Algorithm"),
        ("9", "References"),
    ]
    for num, title in toc:
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, f"  {num}.  {title}", new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════════════════
    # SECTION 1: System Overview
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "System Overview Algorithm")
    pdf.body_text(
        "The Neuro Agentic AI system processes brain MRI/CT images through a multi-agent pipeline "
        "to detect and classify brain tumors. The system supports two parallel pipelines: a local CNN-based "
        "classification pipeline and a Gemini Vision multimodal LLM pipeline."
    )
    pdf.code_block([
        "INPUT  : Brain MRI/CT image (JPEG, PNG, or WebP, <= 10 MB)",
        "OUTPUT : Tumor classification, clinical explanation, GradCAM heatmap, PDF report",
        "",
        "BEGIN",
        "  1. User uploads MRI image via React frontend",
        "  2. Frontend validates file type and encodes as multipart/form-data",
        "  3. FastAPI backend receives and validates the upload",
        "  4. Route to Pipeline A (Local CNN) or Pipeline B (Gemini Vision)",
        "  5. Store result in SQLite audit trail",
        "  6. Return structured JSON response to frontend",
        "  7. Frontend renders results (cards, heatmap, downloadable PDF)",
        "END",
    ])

    pdf.sub_section("System Flow Diagram")
    flow_items = [
        ("User Upload", "MRI image via React UI (click or drag-drop)"),
        ("Frontend Validation", "File type check, base64 encoding, multipart/form-data"),
        ("API Gateway", "FastAPI: CORS, rate limiting (60/min), file size <= 10 MB"),
        ("Pipeline Selection", "Route to CNN Pipeline OR Gemini Vision Pipeline"),
        ("Result Assembly", "JSON response with prediction, explanation, heatmap, disclaimer"),
        ("Database Logging", "SQLite: analysis_history table (audit trail)"),
        ("Frontend Rendering", "PredictionCard, GeminiResultCard, GradCAMCanvas, PDF download"),
    ]
    for i, (title, desc) in enumerate(flow_items):
        if pdf.get_y() > 255:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(0, 71, 161)
        pdf.cell(8, 5, f"{i+1}.", align="R")
        pdf.cell(2, 5, "")
        pdf.set_text_color(40, 40, 40)
        pdf.cell(45, 5, title)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        safe_desc = desc.encode("latin-1", "replace").decode("latin-1")
        pdf.cell(0, 5, f"- {safe_desc}", new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════════════════
    # SECTION 2: Pipeline A - Local CNN
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2", "Pipeline A - Local CNN Classification")
    pdf.body_text(
        "The local CNN pipeline uses a Sequential Multi-Agent Pattern where four specialized agents "
        "process the image in order: Vision Agent, Explainability Agent, Reasoning Agent, and Report Agent. "
        "Each agent receives the output of its predecessor and adds its own analysis layer."
    )

    # Step 1
    pdf.step_box("1", "VISION AGENT (CNN Inference)", [
        "1.1  Load image using PIL -> convert to RGB (ensure 3 channels)",
        "1.2  Resize to 224 x 224 pixels",
        "1.3  Convert to tensor: [0, 255] -> [0, 1]",
        "1.4  Normalize using ImageNet statistics:",
        "       mean = [0.485, 0.456, 0.406]",
        "       std  = [0.229, 0.224, 0.225]",
        "1.5  Add batch dimension -> shape: [1, 3, 224, 224]",
        "1.6  Forward pass through model (ResNet-18 or EfficientNet-B3)",
        "       -> logits: [1, 4]",
        "1.7  Apply Softmax -> probabilities: [4]",
        "1.8  predicted_class = argmax(probabilities)",
        "       Classes: {glioma, meningioma, notumor, pituitary}",
        "1.9  confidence = max(probabilities) x 100",
        "OUTPUT: { predicted_class, confidence, probabilities, tensor }",
    ])

    pdf.arrow_line()

    # Step 2
    pdf.step_box("2", "EXPLAINABILITY AGENT (GradCAM)", [
        "2.1   Select target layer: model.layer4[-1]",
        "        (final residual block of ResNet-18)",
        "2.2   Register forward hooks to capture activations A^k",
        "2.3   Register backward hooks to capture gradients",
        "2.4   Forward pass with gradient tracking enabled",
        "2.5   Backpropagate w.r.t. predicted class score y^c",
        "2.6   Compute channel importance weights:",
        "        alpha_k = (1/Z) * SUM_i SUM_j (dy^c / dA^k_ij)",
        "2.7   Compute weighted activation map:",
        "        L_GradCAM = ReLU( SUM_k alpha_k * A^k )",
        "2.8   Upsample heatmap to 224 x 224 (bilinear interpolation)",
        "2.9   Normalize heatmap to [0, 1]",
        "2.10  Overlay heatmap on original image",
        "OUTPUT: { heatmap (grayscale), overlay (RGB) }",
    ])

    pdf.add_page()
    pdf.arrow_line()

    # Step 3
    pdf.step_box("3", "REASONING AGENT (LLM Explanation)", [
        "3.1  Format probability summary string:",
        "       'glioma: 87.3%, meningioma: 8.6%, ...'",
        "3.2  Construct prompt with predicted_class, confidence,",
        "       and probability distribution",
        "3.3  Send text prompt to Gemini 2.5-Flash API",
        "3.4  IF API call fails -> return static fallback text:",
        "       'The model predicts {class} with {conf}% confidence.",
        "        Please consult a qualified neuroradiologist.'",
        "OUTPUT: explanation (3-4 sentence clinical summary)",
    ])

    pdf.arrow_line()

    # Step 4
    pdf.step_box("4", "REPORT AGENT (Document Compilation)", [
        "4.1  Compile prediction + explanation into structured text",
        "4.2  Add timestamp and medical disclaimer",
        "4.3  Generate PDF (single-page format):",
        "       - Scan information (filename, timestamp)",
        "       - AI diagnosis + confidence percentage",
        "       - Probability distribution table",
        "       - AI explanation paragraph",
        "       - Medical disclaimer footer",
        "OUTPUT: { text_report, pdf_bytes }",
    ])

    # ═══════════════════════════════════════════════════════
    # SECTION 3: Pipeline B - Gemini Vision
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3", "Pipeline B - Gemini Vision Analysis")
    pdf.body_text(
        "The Gemini Vision pipeline uses Google's Gemini 2.5-Flash multimodal LLM for direct "
        "vision-based tumor analysis. The image is sent alongside a structured prompt requesting "
        "a JSON response with tumor metadata, clinical information, and synthetic GradCAM regions."
    )

    # Step 1
    pdf.step_box("1", "IMAGE ENCODING", [
        "1.1  Read raw image bytes from disk",
        "1.2  Detect MIME type (image/jpeg, image/png, image/webp)",
        "1.3  Encode image as base64 for frontend display",
    ])

    pdf.arrow_line()

    # Step 2
    pdf.step_box("2", "MULTIMODAL PROMPT CONSTRUCTION", [
        "2.1  System role: 'Expert neuroradiologist AI'",
        "2.2  Build multimodal content array:",
        "       Part 1: Image bytes + MIME type",
        "       Part 2: Structured prompt requesting JSON",
        "2.3  Required JSON output fields:",
        "       tumorType     - Tumor name (e.g., Glioblastoma Multiforme)",
        "       confidence    - Confidence level (e.g., High ~87%)",
        "       region        - Brain region (e.g., Right Temporal Lobe)",
        "       grade         - WHO grade (e.g., Grade IV)",
        "       whatIsIt       - 3-4 sentence explanation of tumor type",
        "       whyItOccurred  - 3-4 sentences on risk factors",
        "       symptoms       - 3-4 sentences on clinical symptoms",
        "       treatment      - 3-4 sentences on treatment protocols",
        "       prognosis      - 2-3 sentences on survival statistics",
        "       gradcamRegions - Array of 4-8 activation hotspot objects",
        "                        { x, y, w, h, intensity } normalized 0-1",
    ])

    pdf.arrow_line()

    # Step 3
    if pdf.get_y() > 170:
        pdf.add_page()
    pdf.step_box("3", "API CALL WITH RETRY LOGIC", [
        "3.1  models_to_try = [gemini-2.5-flash, gemini-2.5-flash-lite]",
        "3.2  FOR EACH model IN models_to_try:",
        "       FOR attempt = 0 TO 3:",
        "         TRY:",
        "           response = generate_content(model, content)",
        "           raw_text = response.text",
        "           Strip markdown code fences if present (```json...```)",
        "           RETURN json.loads(raw_text)",
        "         CATCH RateLimitError (HTTP 429 / RESOURCE_EXHAUSTED):",
        "           wait = 2^attempt x 2 seconds",
        "           sleep(wait)   // Exponential backoff: 2, 4, 8, 16s",
        "           CONTINUE to next attempt",
        "         CATCH OtherError:",
        "           RAISE to caller",
        "3.3  IF all retries exhausted -> raise RuntimeError",
    ])

    pdf.arrow_line()

    # Step 4
    pdf.step_box("4", "SYNTHETIC GRADCAM REGIONS", [
        "4.1  Gemini returns 4-8 activation hotspot regions",
        "4.2  Each region: { x, y, w, h, intensity }",
        "       (normalized 0-1 relative to image dimensions)",
        "4.3  Highest-intensity region = suspected tumor location",
        "4.4  Frontend renders using jet colormap:",
        "       R = max(0, 1.5 - |4t - 3|)",
        "       G = max(0, 1.5 - |4t - 2|)",
        "       B = max(0, 1.5 - |4t - 1|)   where t = intensity",
        "4.5  Composite onto original image at 55% opacity",
        "4.6  Draw green bounding box around strongest region",
    ])

    pdf.add_page()
    pdf.arrow_line()

    # Step 5
    pdf.step_box("5", "PDF REPORT GENERATION (Multi-Page)", [
        "Page 1 - Detection Summary:",
        "   Disclaimer banner (yellow) | Patient info + timestamp",
        "   Detection: Tumor Type, Confidence, Region, WHO Grade",
        "   Sections: What Is It / Why It Occurred / Symptoms",
        "",
        "Page 2 - Treatment & Prognosis:",
        "   Treatment protocols section",
        "   Prognosis & survival statistics",
        "   GradCAM activation regions table",
        "     | Region # | X    | Y    | W    | H    | Intensity |",
        "",
        "Page 3 - Legal Disclaimers:",
        "   Medical disclaimer | Accuracy limitations",
        "   Privacy notice | Emergency contact information",
    ])

    # ═══════════════════════════════════════════════════════
    # SECTION 4: Classification Model Architecture
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("4", "Classification Model Architecture")
    pdf.body_text(
        "The system supports two pre-trained convolutional neural network architectures for 4-class "
        "brain tumor classification: ResNet-18 and EfficientNet-B3. Both models are fine-tuned on brain "
        "MRI datasets with modified classification heads."
    )

    # Model comparison table
    pdf.sub_section("Model Comparison")
    widths = [40, 30, 25, 25, 35, 35]
    headers = ["Model", "Layers", "Input", "Classes", "Final FC In", "Weights File"]
    pdf.table_row(headers, widths, bold=True, fill=True)
    pdf.table_row(["ResNet-18", "18", "224x224x3", "4", "512", "brain_tumor_resnet18.pth"], widths)
    pdf.table_row(["EfficientNet-B3", "~50", "224x224x3", "4", "1536", "brain_tumor_efficientnet_b3.pth"], widths)
    pdf.ln(5)

    # ResNet-18
    pdf.sub_section("Option A: ResNet-18 Architecture")
    pdf.code_block([
        "Input: [1, 3, 224, 224]",
        "  -> Conv1 (7x7, stride 2) -> BatchNorm -> ReLU -> MaxPool(3x3, stride 2)",
        "  -> Layer1: 2x BasicBlock (64 filters, 3x3 conv)",
        "  -> Layer2: 2x BasicBlock (128 filters, 3x3 conv, downsample)",
        "  -> Layer3: 2x BasicBlock (256 filters, 3x3 conv, downsample)",
        "  -> Layer4: 2x BasicBlock (512 filters, 3x3 conv, downsample)",
        "  -> AdaptiveAvgPool2d(1,1) -> Flatten -> [1, 512]",
        "  -> FC(512, 4)    // Modified: original FC(512, 1000) replaced",
        "  -> Softmax -> [p_glioma, p_meningioma, p_notumor, p_pituitary]",
    ])

    # EfficientNet-B3
    pdf.sub_section("Option B: EfficientNet-B3 Architecture")
    pdf.code_block([
        "Input: [1, 3, 224, 224]",
        "  -> Stem Conv (3x3, stride 2) -> BatchNorm -> SiLU activation",
        "  -> 7x MBConv Blocks (compound scaling: width, depth, resolution)",
        "     - Depthwise separable convolutions (reduces parameters)",
        "     - Squeeze-and-Excitation modules (channel attention)",
        "     - Stochastic depth regularization (drop path)",
        "     - Inverted residual connections",
        "  -> Head Conv (1x1) -> BatchNorm -> SiLU",
        "  -> AdaptiveAvgPool2d(1,1) -> Flatten -> [1, 1536]",
        "  -> Dropout(0.3) -> FC(1536, 4)    // Modified classifier head",
        "  -> Softmax -> [p_glioma, p_meningioma, p_notumor, p_pituitary]",
    ])

    pdf.sub_section("Classification Classes")
    pdf.code_block([
        "CLASS_NAMES = ['glioma', 'meningioma', 'notumor', 'pituitary']",
        "",
        "  Index 0: glioma      - Primary brain tumor from glial cells",
        "  Index 1: meningioma   - Tumor arising from meninges",
        "  Index 2: notumor      - No tumor detected (healthy scan)",
        "  Index 3: pituitary    - Tumor of the pituitary gland",
    ])

    pdf.sub_section("Image Preprocessing Pipeline")
    pdf.code_block([
        "transforms.Compose([",
        "    transforms.Resize((224, 224)),          # Spatial resize",
        "    transforms.ToTensor(),                   # [0,255] -> [0,1], HWC -> CHW",
        "    transforms.Normalize(",
        "        mean=[0.485, 0.456, 0.406],         # ImageNet channel means",
        "        std=[0.229, 0.224, 0.225]            # ImageNet channel stds",
        "    )",
        "])",
        "",
        "# Result: Tensor shape [1, 3, 224, 224] on GPU/CPU device",
    ])

    # ═══════════════════════════════════════════════════════
    # SECTION 5: GradCAM Algorithm
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5", "GradCAM Heatmap Algorithm")
    pdf.body_text(
        "Gradient-weighted Class Activation Mapping (GradCAM) is used to produce visual explanations "
        "highlighting which regions of the MRI image most influenced the model's prediction. The "
        "implementation follows Selvaraju et al. (2017) and uses the pytorch-grad-cam library."
    )

    pdf.sub_section("Reference")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5, 'Selvaraju, R.R., et al. "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization" (ICCV 2017)')
    pdf.ln(3)

    pdf.sub_section("Formal Algorithm")
    pdf.code_block([
        "ALGORITHM: Gradient-weighted Class Activation Mapping (GradCAM)",
        "INPUT  : Model M, Input image X, Target class c, Target layer L",
        "OUTPUT : Heatmap H (same spatial dimensions as X)",
        "",
        "BEGIN",
        "  1.  Forward pass: Compute feature maps A^k at layer L",
        "      (k = 1, ..., K channels; each A^k has spatial size u x v)",
        "",
        "  2.  Compute class score y^c (logit for class c before softmax)",
        "",
        "  3.  Backward pass: Compute gradients dy^c / dA^k_ij",
        "",
        "  4.  Global average pooling of gradients (importance weights):",
        "",
        "      alpha_k^c = (1 / Z) * SUM_i SUM_j (dy^c / dA^k_ij)",
        "",
        "      where Z = u * v (number of spatial positions)",
        "",
        "  5.  Weighted combination of forward activation maps:",
        "",
        "      L_GradCAM = ReLU( SUM_k  alpha_k^c * A^k )",
        "",
        "      ReLU retains only features with positive influence on class c",
        "",
        "  6.  Upsample L_GradCAM to input resolution (224 x 224)",
        "      using bilinear interpolation",
        "",
        "  7.  Normalize to [0, 1]:",
        "      H = (L_GradCAM - min) / (max - min)",
        "",
        "  8.  Create visualization overlay:",
        "      Overlay = alpha * JetColormap(H) + (1 - alpha) * OriginalImage",
        "      where alpha = blending factor (typically 0.4-0.6)",
        "END",
    ])

    pdf.sub_section("Implementation Details")
    pdf.code_block([
        "Target layer:  model.layer4[-1]  (ResNet-18 final residual block)",
        "Library:       pytorch-grad-cam (GradCAM class)",
        "Target:        ClassifierOutputTarget(predicted_idx)",
        "Overlay:       show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)",
    ])

    # ═══════════════════════════════════════════════════════
    # SECTION 6: Batch & Multi-Patient
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6", "Batch & Multi-Patient Processing Algorithm")

    pdf.sub_section("Algorithm A: Batch Analysis with Conflict Detection")
    pdf.code_block([
        "ALGORITHM: Batch Analysis with Conflict Detection",
        "INPUT  : files[] (multiple MRI images for one patient)",
        "OUTPUT : results[] with optional conflict warnings",
        "",
        "BEGIN",
        "  1.  FOR EACH file IN files[]:",
        "        result[i] = GeminiVisionAgent.analyze(file)",
        "",
        "  2.  CONFLICT DETECTION:",
        "      tumor_types = { result[i].tumorType  for all i }",
        "      Remove 'no tumor' entries from set",
        "",
        "      IF |tumor_types| > 1:",
        "        FLAG WARNING: 'Conflicting diagnoses detected.",
        "        Verify all scans belong to the same patient.'",
        "",
        "  3.  RETURN { results[], conflicts (if any) }",
        "END",
    ])

    pdf.sub_section("Algorithm B: Diagnostic Center (Multi-Patient)")
    pdf.code_block([
        "ALGORITHM: Diagnostic Center (Multi-Patient Batch)",
        "INPUT  : patients[] (each with name and files[])",
        "OUTPUT : patient_results[]",
        "",
        "BEGIN",
        "  FOR EACH patient IN patients[]:",
        "    1.  Validate patient.files (type, size constraints)",
        "    2.  Run Batch Analysis with Conflict Detection (Algorithm A)",
        "    3.  Update progress bar: (completed / total) x 100%",
        "    4.  Store results per patient",
        "",
        "  RETURN patient_results[]",
        "END",
    ])

    pdf.sub_section("Conflict Detection Logic")
    pdf.body_text(
        "When multiple scans are submitted for the same patient, the system checks for diagnostic "
        "consistency. If two or more different tumor types are detected across scans (excluding 'no tumor' "
        "results), the system flags a warning suggesting the user verify that all scans belong to the "
        "same patient. This prevents misdiagnosis from mixed scan sets."
    )

    # ═══════════════════════════════════════════════════════
    # SECTION 7: PDF Report Generation
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7", "PDF Report Generation Algorithm")

    pdf.sub_section("Algorithm: PDF Report Generation (FPDF)")
    pdf.code_block([
        "ALGORITHM: PDF Report Generation",
        "INPUT  : analysis result (CNN prediction OR Gemini output)",
        "OUTPUT : PDF binary stream",
        "",
        "BEGIN",
        "  1.  Initialize FPDF with A4 portrait, UTF-8 safe mode",
        "  2.  Sanitize all text:",
        "        Replace Unicode chars -> Latin-1 equivalents",
        "        (en-dash, smart quotes, ellipsis, etc.)",
        "",
        "  3.  IF source == 'CNN Pipeline':",
        "        Single-page layout:",
        "          - Header + scan metadata",
        "          - Diagnosis + confidence percentage",
        "          - Class probability distribution table",
        "          - AI explanation paragraph",
        "          - Medical disclaimer footer",
        "",
        "  4.  IF source == 'Gemini Pipeline':",
        "        Page 1 -- Detection Summary:",
        "          - Disclaimer banner (yellow background)",
        "          - Patient info + timestamp",
        "          - Detection metrics table:",
        "            Tumor Type | Confidence | Region | WHO Grade",
        "          - Sections: What Is It / Why Occurred / Symptoms",
        "",
        "        Page 2 -- Treatment & Prognosis:",
        "          - Treatment protocols section",
        "          - Prognosis & survival statistics",
        "          - GradCAM activation regions table:",
        "            Region# | X | Y | W | H | Intensity",
        "",
        "        Page 3 -- Legal Disclaimers:",
        "          - Medical disclaimer",
        "          - Accuracy limitations",
        "          - Privacy notice (not HIPAA/GDPR certified)",
        "          - Emergency contact information",
        "",
        "  5.  RETURN pdf.output() as byte stream",
        "END",
    ])

    # ═══════════════════════════════════════════════════════
    # SECTION 8: API Security
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("8", "API Rate Limiting & Security Algorithm")

    pdf.sub_section("Request Validation Pipeline")
    pdf.code_block([
        "ALGORITHM: Request Validation & Rate Limiting",
        "",
        "BEGIN",
        "  FOR EACH incoming HTTP request:",
        "",
        "    1.  CORS Validation:",
        "          Check Origin header against allowed_origins list",
        "          IF not allowed -> reject with 403 Forbidden",
        "",
        "    2.  Rate Limit Check:",
        "          Limit: 60 requests per minute (global, via SlowAPI)",
        "          IF exceeded -> return 429 Too Many Requests",
        "",
        "    3.  File Validation:",
        "          a. Check extension:",
        "             ALLOWED = {.jpg, .jpeg, .png, .webp}",
        "             IF ext NOT IN ALLOWED -> return 400 Bad Request",
        "",
        "          b. Check file size:",
        "             Stream file in 8192-byte chunks",
        "             IF total > 10 MB -> return 413 Payload Too Large",
        "",
        "    4.  File Handling:",
        "          Save to uploads/ directory with original filename",
        "          Process through selected pipeline",
        "",
        "    5.  Audit Logging:",
        "          INSERT INTO analysis_history (",
        "            filename, prediction, confidence, timestamp",
        "          )",
        "",
        "    6.  Cleanup:",
        "          Remove temporary upload files",
        "",
        "    7.  Response:",
        "          Return JSON with results + medical disclaimer",
        "END",
    ])

    pdf.sub_section("API Endpoints Summary")
    widths2 = [45, 15, 55, 55]
    pdf.table_row(["Endpoint", "Method", "Purpose", "Response"], widths2, bold=True, fill=True)
    pdf.table_row(["/analyze", "POST", "Single CNN inference", "prediction + explanation"], widths2)
    pdf.table_row(["/analyze/batch", "POST", "Multiple CNN inferences", "results array"], widths2)
    pdf.table_row(["/analyze/gemini", "POST", "Single Gemini analysis", "structured analysis JSON"], widths2)
    pdf.table_row(["/analyze/gemini/batch", "POST", "Multiple Gemini analyses", "results array"], widths2)
    pdf.table_row(["/analyze/download-pdf", "POST", "Generate CNN report PDF", "binary PDF stream"], widths2)
    pdf.table_row(["/analyze/gemini/download-pdf", "POST", "Generate Gemini PDF", "binary PDF stream"], widths2)
    pdf.table_row(["/analyze/history", "GET", "Audit trail", "history array"], widths2)
    pdf.table_row(["/health", "GET", "Health check", "{status: ok}"], widths2)

    pdf.ln(6)
    pdf.sub_section("Error Response Codes")
    widths3 = [30, 60, 80]
    pdf.table_row(["Code", "Condition", "Message"], widths3, bold=True, fill=True)
    pdf.table_row(["400", "Unsupported file extension", "Unsupported file type. Allowed: jpg, jpeg, png, webp"], widths3)
    pdf.table_row(["413", "File exceeds size limit", "File too large. Maximum size is 10 MB."], widths3)
    pdf.table_row(["429", "Rate limit exceeded", "Too many requests. Please try again later."], widths3)
    pdf.table_row(["500", "Internal server error", "An internal server error occurred."], widths3)

    # ═══════════════════════════════════════════════════════
    # SECTION 9: References
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("9", "References")
    pdf.body_text("The following technical references informed the model architecture, explainability method, and implementation stack.")
    pdf.code_block([
        "[1] He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR.",
        "[2] Tan, M., Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. ICML.",
        "[3] Selvaraju, R.R., et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. ICCV.",
        "[4] Simonyan, K., Zisserman, A. (2015). Very Deep Convolutional Networks for Large-Scale Image Recognition.",
        "[5] FastAPI Documentation: https://fastapi.tiangolo.com/",
        "[6] PyTorch Documentation: https://pytorch.org/docs/stable/",
        "[7] pytorch-grad-cam Documentation: https://github.com/jacobgil/pytorch-grad-cam",
        "[8] Google Gemini API Documentation: https://ai.google.dev/gemini-api/docs",
    ])

    # Save
    output_path = "Neuro_Agentic_AI_Algorithm_Documentation.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_pdf()
