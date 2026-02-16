from fastapi import FastAPI
from api.health import router as health_router
from api.analyze import router as analyze_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Neuro Diagnosis Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
@app.get("/")

def root():
    return {"message": "Backend is running"}
