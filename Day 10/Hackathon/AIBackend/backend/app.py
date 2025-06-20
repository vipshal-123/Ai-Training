import logging
from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.lifespan import lifespan
from backend.routes.index import router as api_routes

logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv

load_dotenv("local.env")

app = FastAPI(
    lifespan=lifespan,
    title="Elevator Pitch Generator API",
    description="API for generating personalized student elevator pitches and recruiter insights.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={"name": "vipshal", "url": "http://localhost:5002"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_checker(request: Request, call_next):
    data = await request.body()
    logging.info(data)
    return await call_next(request)


app.include_router(prefix="/api", router=api_routes)
