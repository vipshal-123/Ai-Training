from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from backend.config.main import CORS_ORIGIN, MONGO_URI
import logging

from backend.models.User import User
from backend.models.UploadedFile import UploadedFile 
from backend.models.Candidate import Candidate
from backend.models.AnalysisResult import AnalysisResult


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = AsyncIOMotorClient(MONGO_URI)["ai-workshop"]
    await init_beanie(
        database=app.db,
        document_models=[
            User,
            UploadedFile,
            Candidate,
            AnalysisResult
        ],
    )
    logging.info("Database initialized")
    yield
    logging.info("Server closed successfully")
