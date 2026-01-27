import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, UnidentifiedImageError

from app.config.settings import (
    MODEL_ARCHITECTURE,
    MODEL_PATHS,
    NUM_CLASSES,
    CLASS_NAMES,
    IMAGE_SIZE,
    MEAN,
    STD,
)


class VisionAgent:
    """
    Handles model loading, preprocessing, and inference
    Supports ResNet-18 and EfficientNet-B3
    """

    def __init__(self):
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = self._get_transform()

    def _get_transform(self):
        return transforms.Compose([
            transforms.Resize(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=MEAN, std=STD),
        ])

    def _build_model(self):
        if MODEL_ARCHITECTURE == "resnet18":
            model = models.resnet18(weights=None)
            model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)

        elif MODEL_ARCHITECTURE == "efficientnet_b3":
            model = models.efficientnet_b3(weights=None)
            model.classifier[1] = nn.Linear(
                model.classifier[1].in_features, NUM_CLASSES
            )

        else:
            raise ValueError(f"Unsupported model: {MODEL_ARCHITECTURE}")

        return model

    def load_model(self):
        if self.model is not None:
            return self.model

        model_path = MODEL_PATHS[MODEL_ARCHITECTURE]

        self.model = self._build_model()
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint)

        self.model.to(self.device)
        self.model.eval()
        return self.model

    def preprocess_image(self, image_path):
        try:
            image = Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
            raise ValueError(f"File is not a valid image: {image_path}")
        except Exception as e:
            raise ValueError(f"Failed to load image {image_path}: {e}")

        tensor = self.transform(image).unsqueeze(0)
        return tensor.to(self.device), image

    def predict(self, image_path):
        if self.model is None:
            self.load_model()

        tensor, original_image = self.preprocess_image(image_path)

        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

        predicted_idx = int(probabilities.argmax())
        predicted_class = CLASS_NAMES[predicted_idx]
        confidence = float(probabilities[predicted_idx] * 100)

        return {
            "probabilities": probabilities,
            "predicted_class": predicted_class,
            "predicted_idx": predicted_idx,
            "confidence": confidence,
            "original_image": original_image,
            "class_names": CLASS_NAMES,
            "preprocessed_tensor": tensor,
        }

    def get_model_for_gradcam(self):
        if self.model is None:
            self.load_model()
        return self.model
