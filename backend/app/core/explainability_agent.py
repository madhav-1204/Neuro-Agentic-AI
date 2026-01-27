import torch
import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

from app.config.settings import IMAGE_SIZE


class ExplainabilityAgent:
    """
    Generates Grad-CAM visualizations
    """

    def __init__(self, model):
        self.model = model

    def _get_target_layer(self):
        return [self.model.layer4[-1]]

    def generate_gradcam(self, image_tensor, predicted_idx):
        with GradCAM(
            model=self.model, target_layers=self._get_target_layer()
        ) as cam:
            targets = [ClassifierOutputTarget(predicted_idx)]
            grayscale_cam = cam(input_tensor=image_tensor, targets=targets)[0]
        return grayscale_cam

    def create_overlay(self, original_image, grayscale_cam):
        img = original_image.resize(IMAGE_SIZE)
        rgb_img = np.array(img).astype(np.float32) / 255.0
        return show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)

    def explain(self, image_tensor, original_image, predicted_idx):
        cam = self.generate_gradcam(image_tensor, predicted_idx)
        overlay = self.create_overlay(original_image, cam)
        return {
            "heatmap": cam,
            "overlay": overlay,
            "explanation": "Highlighted regions influenced the prediction.",
        }
