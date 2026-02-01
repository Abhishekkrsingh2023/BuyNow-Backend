import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import Users,Carts,Orders,Products

async def migrate():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["Shopping-App"]

    await init_beanie(database=db, document_models=[
        Users,
        Carts,
        Orders,
        Products
    ])

    # Update documents that do NOT have alternateNo
    result = await Users.find(
        {"alternateNo": {"$exists": False}}
    ).update(
        {"$set": {"alternateNo": None}}
    )

    print("Migration complete:", result)

if __name__ == "__main__":
    asyncio.run(migrate())
