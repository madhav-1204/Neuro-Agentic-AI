import os
from dotenv import load_dotenv

load_dotenv(override=True)

# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
# BASE_DIR -> backend/

# =========================
# Model Selection
# =========================

MODEL_ARCHITECTURE = "resnet18"

MODEL_PATHS = {
    "resnet18": os.path.join(BASE_DIR, "models", "brain_tumor_resnet18.pth"),
    "efficientnet_b3": os.path.join(
        BASE_DIR, "models", "brain_tumor_efficientnet_b3.pth"
    ),
}

NUM_CLASSES = 4


# =========================
# Classes
# =========================

CLASS_NAMES = ['glioma', 'meningioma', 'notumor', 'pituitary']

# =========================
# Image preprocessing
# =========================

IMAGE_SIZE = (224, 224)
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# =========================
# LLM
# =========================

GEMINI_MODEL = "gemini-2.5-flash"

# =========================
# Authentication
# =========================

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Google OAuth Settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
