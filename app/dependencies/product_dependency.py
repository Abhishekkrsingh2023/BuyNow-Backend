import asyncio
import os, uuid

from fastapi import (
    Depends, 
    HTTPException, 
    Form, 
    File,
    UploadFile
)
from beanie import BeanieObjectId

from app.utils.cloudinary_file_upload import upload_file_to_cloudinary
from app.schemas import Products
from app.auth_dependency.auth_user import authenticate_user



ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def _upload_one_image(image: UploadFile) -> dict | None:
    """
    Saves UploadFile to a temp file, uploads to Cloudinary in a thread (non-blocking),
    and cleans up the temp file reliably.
    Returns {"url": ..., "imgId": ...} or None if upload failed.
    """
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported image type: {image.content_type}")

    suffix = ""
    if image.filename:
        _, ext = os.path.splitext(image.filename)
        suffix = ext or ""

    temp_path = None
    try:
        os.makedirs("temp", exist_ok=True)
        temp_id = str(uuid.uuid4())
        temp_filename = f"{temp_id}{suffix}"
        temp_path = os.path.join("temp", temp_filename)

        with open(temp_path, "wb") as tmp:
            tmp.write(await image.read())
            tmp.flush()

        # Offload sync upload to a worker thread so FastAPI event loop isn't blocked
        upload_result = await asyncio.to_thread(upload_file_to_cloudinary, file_path=temp_path, public_id=temp_id)

        if not upload_result:
            return None

        return {
            "url": upload_result.get("secure_url"),
            "imgId": upload_result.get("public_id"),
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                pass


async def create_product_dependency(
    name: str = Form(...),
    description: str = Form(...),
    selling_price: float = Form(...),
    mrp: float = Form(...),
    quantity: int = Form(...),
    in_stock: bool = Form(True),
    images: list[UploadFile] = File(...),
    token: dict = Depends(authenticate_user),
):
    role = token.get("role")
    seller_id = token.get("id")

    if role != "seller":
        raise HTTPException(status_code=403, detail="Operation forbidden: Sellers only")
    
    if selling_price < 0 or mrp < 0 or quantity < 0:
        raise HTTPException(status_code=400, detail="Price/quantity must be non-negative")
    
    if selling_price > mrp:
        raise HTTPException(status_code=400, detail="Selling price cannot exceed MRP")

    # Upload images concurrently
    upload_tasks = [asyncio.create_task(_upload_one_image(img)) for img in images]
    results = await asyncio.gather(*upload_tasks)

    uploaded_images = [r for r in results if r is not None]
    if not uploaded_images:
        raise HTTPException(status_code=400, detail="No images were uploaded")

    new_product = Products(
        sellerID=seller_id,
        name=name,
        description=description,
        sellingPrice=selling_price,
        mrp=mrp,
        quantity=quantity,
        in_stock=in_stock,
        imageUrl=uploaded_images,
    )

    await new_product.insert()
    return {"message": "success", "product": new_product}

async def get_product_dependency(
    token: dict = Depends(authenticate_user),
):
    role = token.get("role")
    seller_id = token.get("id")

    if role != "seller":
        raise HTTPException(status_code=403, detail="Operation forbidden: Sellers only")

    seller_oid = BeanieObjectId(seller_id)
    products = await Products.find(Products.sellerID.id == seller_oid).to_list()
    return products


async def get_random_products_dependency(limit: int = 10):
    limit = max(1, int(limit))

    pipeline = [
        {
            "$match": {"in_stock": True}
        },
        {
            "$sample": {"size": limit}
        }
    ]

    collection = Products.get_pymongo_collection()
    cursor = collection.aggregate(pipeline)
    products = await cursor.to_list(length=limit)

    # handling IDs
    for p in products:
        p["id"] = str(p.pop("_id"))
        sellerID = str(p["sellerID"].id)
        p["sellerID"] = sellerID

    return products

async def get_product_by_id_dependency(id: BeanieObjectId):
    product = await Products.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product