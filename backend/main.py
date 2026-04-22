from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routers import fortune, donation, admin

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="宮廟抽籤系統 API", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For MVP, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fortune.router, prefix="/api/v1")
app.include_router(donation.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount static files
from fastapi.staticfiles import StaticFiles
import os

if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

