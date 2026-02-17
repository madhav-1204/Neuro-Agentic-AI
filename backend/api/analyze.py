import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.core.orchestrator import Orchestrator
from app.services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()

UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "uploads",
)
os.makedirs(UPLOAD_DIR, exist_ok=True)

orch = Orchestrator()
orch.load_model()


def save_upload(file: UploadFile):
    ext = os.path.splitext(file.filename)[1]
    name = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, name)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path, file.filename


@router.post("/analyze")
def analyze_single(file: UploadFile = File(...)):
    path, original_name = save_upload(file)

    try:
        res = orch.process_image(path)
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
        }
    except ValueError as e:
        return {"filename": original_name, "error": str(e)}
    finally:
        os.remove(path)


@router.post("/analyze/batch")
def analyze_batch(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        path, original_name = save_upload(file)

        try:
            res = orch.process_image(path)
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
            os.remove(path)

    return {"results": results}


@router.post("/analyze/download-pdf")
def download_pdf(result: dict):
    """Generate and download a PDF report from analysis results"""
    try:
        pdf_path = pdf_service.generate_single_scan_pdf(result)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_path),
        )
    except Exception as e:
        return {"error": f"Failed to generate PDF: {str(e)}"}
