import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File
from app.core.orchestrator import Orchestrator

router = APIRouter()

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
