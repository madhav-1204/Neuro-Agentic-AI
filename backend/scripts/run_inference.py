import json
import sys
import os
import numpy as np

# Ensure backend/app is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app.core.orchestrator import Orchestrator


def to_json_safe(obj):
    """Convert objects into JSON-serializable structures"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (float, int, str, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_json_safe(v) for v in obj]
    return None


def extract_prediction(pred):
    """DTO for prediction"""
    return {
        "predicted_class": pred["predicted_class"],
        "predicted_idx": int(pred["predicted_idx"]),
        "confidence": float(pred["confidence"]),
        "class_names": list(pred["class_names"]),
        "probabilities": to_json_safe(pred["probabilities"]),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass a JSON list of image paths"}))
        return

    try:
        image_paths = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        return

    orch = Orchestrator()
    orch.load_model()

    results = []

    for path in image_paths:
        if not os.path.exists(path):
            results.append(
                {"filename": os.path.basename(path), "error": "File not found"}
            )
            continue

        try:
            res = orch.process_image(path)

            results.append(
                {
                    "filename": os.path.basename(path),
                    "prediction": extract_prediction(res["prediction"]),
                    "explanation": str(res["explanation"]),
                }
            )

        except ValueError as e:
            # Handles non-image files and other validation errors
            results.append(
                {
                    "filename": os.path.basename(path),
                    "error": str(e),
                }
            )

    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    main()
