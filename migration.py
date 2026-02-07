from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

PRODUCTS_COLLECTION = "products"

async def migrate_products():
    """
    One-time migration to backfill new Product fields and rename imageUrl -> images.
    Uses raw MongoDB updates to avoid Beanie/Pydantic validation issues on old docs.
    """
    client = AsyncIOMotorClient(settings.MONGO_URL)
    try:
        db = client[settings.DATABASE_NAME]
        col = db[PRODUCTS_COLLECTION]

        # 1) Backfill missing fields
        await col.update_many(
            {"category": {"$exists": False}},
            {"$set": {"category": "Uncategorized"}},
        )
        await col.update_many(
            {"subcategory": {"$exists": False}},
            {"$set": {"subcategory": []}},
        )

        # 2) Migrate imageUrl -> images (only where images doesn't exist yet)
        await col.update_many(
            {"images": {"$exists": False}},
            [
                {"$set": {"images": {"$ifNull": ["$imageUrl", []]}}},
                {"$unset": "imageUrl"},
            ],
        )

        # 3) Optional cleanup: if any docs still have imageUrl, remove it
        await col.update_many(
            {"imageUrl": {"$exists": True}},
            {"$unset": {"imageUrl": ""}},
        )

        print("Product migration completed.")
    finally:
        client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(migrate_products())