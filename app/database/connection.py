from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config.settings import settings

from app.schemas import (
    Users,
    Carts,
    Products,
    Orders,
)

async def get_database() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)
        await init_beanie(
            client[settings.DATABASE_NAME], 
            document_models=[Users, Carts, Products, Orders],
        )
        return client
    except Exception:
        raise Exception("Database connection failed......")