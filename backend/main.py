import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.health import router as health_router
from api.analyze import router as analyze_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import init_db

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
)
logger = logging.getLogger(__name__)

# ── Rate limiter ────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# ── App ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Neuro Diagnosis Backend",
    version="2.0.0",
    description="AI-powered brain MRI analysis API",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ────────────────────────────────────────────────────────────
_extra_origins = os.getenv("CORS_ORIGINS", "")
allowed_origins = ["http://localhost:5173", "http://localhost:5174"]
if _extra_origins:
    allowed_origins.extend([o.strip() for o in _extra_origins.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global exception handler ───────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "An internal server error occurred. Please try again later.",
        },
    )


# ── Request logging middleware ──────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    return response


# ── Startup ─────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialised, server ready.")


# ── Routers ─────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "Backend is running", "version": "2.0.0"}
