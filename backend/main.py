from fastapi import FastAPI
from api.health import router as health_router
from api.analyze import router as analyze_router

app = FastAPI(
    title="Neuro Diagnosis Backend",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(analyze_router)
@app.get("/")

def root():
    return {"message": "Backend is running"}
