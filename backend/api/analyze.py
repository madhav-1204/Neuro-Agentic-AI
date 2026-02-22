import os
import uuid
import shutil
import base64
import asyncio
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from app.core.orchestrator import Orchestrator
from app.core.gemini_vision_agent import GeminiVisionAgent
from app.services.pdf_service import PDFService
from app.config.settings import MAX_UPLOAD_SIZE_MB, ALLOWED_EXTENSIONS, MEDICAL_DISCLAIMER
from app.database import log_analysis

logger = logging.getLogger(__name__)

router = APIRouter()
pdf_service = PDFService()
vision_agent = GeminiVisionAgent()

UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "uploads",
)
os.makedirs(UPLOAD_DIR, exist_ok=True)

orch = Orchestrator()
orch.load_model()

MAX_UPLOAD_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024


# ── Helpers ─────────────────────────────────────────────────────────

def _validate_file(file: UploadFile):
    """Validate file extension and size."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

def save_upload(file: UploadFile):
    _validate_file(file)
    ext = os.path.splitext(file.filename)[1]
    name = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, name)

    with open(path, "wb") as buffer:
        size = 0
        while chunk := file.file.read(8192):
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                buffer.close()
                os.remove(path)
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size is {MAX_UPLOAD_SIZE_MB} MB.",
                )
            buffer.write(chunk)

    return path, file.filename


# ── Endpoints ───────────────────────────────────────────────────────

@router.post("/analyze")
async def analyze_single(
    file: UploadFile = File(...),
):
    path, original_name = save_upload(file)

    try:
        res = await asyncio.to_thread(orch.process_image, path)
        return {
            "filename": original_name,
            "prediction": {
                "predicted_class": res["prediction"]["predicted_class"],
                "predicted_idx": res["prediction"]["predicted_idx"],
                "confidence": res["prediction"]["confidence"],
                "class_names": res["prediction"]["class_names"],
                "probabilities": res["prediction"]["probabilities"].tolist(),
            },
            "explanation": str(res["explanation"]),
            "disclaimer": MEDICAL_DISCLAIMER,
        }
    except ValueError as e:
        return {"filename": original_name, "error": str(e)}
    finally:
        if os.path.exists(path):
            os.remove(path)


@router.post("/analyze/batch")
async def analyze_batch(
    files: list[UploadFile] = File(...),
):
    results = []

    for file in files:
        path, original_name = save_upload(file)

        try:
            res = await asyncio.to_thread(orch.process_image, path)
            results.append(
                {
                    "filename": original_name,
                    "prediction": {
                        "predicted_class": res["prediction"]["predicted_class"],
                        "predicted_idx": res["prediction"]["predicted_idx"],
                        "confidence": res["prediction"]["confidence"],
                        "class_names": res["prediction"]["class_names"],
                        "probabilities": res["prediction"]["probabilities"].tolist(),
                    },
                    "explanation": str(res["explanation"]),
                }
            )
        except ValueError as e:
            results.append({"filename": original_name, "error": str(e)})
        finally:
            if os.path.exists(path):
                os.remove(path)

    return {"results": results, "disclaimer": MEDICAL_DISCLAIMER}


@router.post("/analyze/gemini")
async def analyze_with_gemini(
    file: UploadFile = File(...),
):
    """
    Analyze a brain MRI using Gemini's vision API.
    Returns structured tumor analysis with GradCAM regions.
    """
    path, original_name = save_upload(file)

    try:
        # Read image for base64 encoding to send back to frontend
        with open(path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        ext = os.path.splitext(original_name)[1].lower()
        media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
        media_type = media_map.get(ext, "image/jpeg")

        # Run Gemini vision analysis in thread (network-bound)
        analysis = await asyncio.to_thread(vision_agent.analyze, path)

        if "error" in analysis:
            return {"filename": original_name, "error": analysis["error"]}

        # Audit trail
        log_analysis("", original_name, analysis)

        return {
            "filename": original_name,
            "image": f"data:{media_type};base64,{image_b64}",
            "analysis": analysis,
            "disclaimer": MEDICAL_DISCLAIMER,
        }
    except Exception as e:
        logger.error("Gemini analysis failed for %s: %s", original_name, e, exc_info=True)
        return {"filename": original_name, "error": str(e)}
    finally:
        if os.path.exists(path):
            os.remove(path)


@router.post("/analyze/gemini/batch")
async def analyze_batch_gemini(
    files: list[UploadFile] = File(...),
):
    """
    Analyze multiple MRI scans from different patients using Gemini Vision.
    Each file is analyzed independently and results returned as a list.
    """
    results = []

    for file in files:
        path, original_name = save_upload(file)

        try:
            with open(path, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode("utf-8")

            ext = os.path.splitext(original_name)[1].lower()
            media_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }
            media_type = media_map.get(ext, "image/jpeg")

            analysis = await asyncio.to_thread(vision_agent.analyze, path)

            if "error" in analysis:
                results.append(
                    {"filename": original_name, "error": analysis["error"]}
                )
            else:
                # Audit trail
                log_analysis("", original_name, analysis)

                results.append(
                    {
                        "filename": original_name,
                        "image": f"data:{media_type};base64,{image_b64}",
                        "analysis": analysis,
                    }
                )
        except Exception as e:
            logger.error("Batch gemini error for %s: %s", original_name, e, exc_info=True)
            results.append({"filename": original_name, "error": str(e)})
        finally:
            if os.path.exists(path):
                os.remove(path)

    return {"results": results, "disclaimer": MEDICAL_DISCLAIMER}


@router.post("/analyze/gemini/download-pdf")
async def download_gemini_pdf(result: dict):
    """Generate and download a 3-page PDF report from Gemini analysis results"""
    try:
        pdf_path = await asyncio.to_thread(pdf_service.generate_claude_report, result)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_path),
        )
    except Exception as e:
        logger.error("PDF generation failed: %s", e, exc_info=True)
        return {"error": f"Failed to generate PDF: {str(e)}"}


@router.post("/analyze/download-pdf")
async def download_pdf(result: dict):
    """Generate and download a PDF report from analysis results"""
    try:
        pdf_path = await asyncio.to_thread(pdf_service.generate_single_scan_pdf, result)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_path),
        )
    except Exception as e:
        logger.error("PDF generation failed: %s", e, exc_info=True)
        return {"error": f"Failed to generate PDF: {str(e)}"}


# ── History endpoint ────────────────────────────────────────────────

@router.get("/analyze/history")
async def get_analysis_history():
    """Return the analysis audit trail."""
    from app.database import get_history
    history = get_history()
    # Strip the full analysis JSON to keep response small
    for h in history:
        h.pop("analysis_json", None)
    return {"history": history}
