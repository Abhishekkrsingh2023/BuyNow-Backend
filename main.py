from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.connection import get_database

from app.api.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        mongo_client = await get_database()
    except Exception as e:
        raise SystemExit(e)

    yield

    mongo_client.close()
    print("Shutting down...")

app = FastAPI(
    title="My API",
    description="This is a sample API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to BuyNow's Backend API!"}
