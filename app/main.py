from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os

app = FastAPI(title="Research Tool API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# LOAD .env FROM PROJECT ROOT (robust method)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(env_path)

# --------------------------------------------------
# IMPORT ROUTES AFTER ENV LOAD
# --------------------------------------------------
from app.routes import router

app = FastAPI(title="Research Tool API")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Research Tool Running"}