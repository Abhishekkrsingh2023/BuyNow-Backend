from beanie import PydanticObjectId
# import os 
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from app.schemas import Products



async def add_category_and_subcategory_to_products():
    products = await Products.find_all().to_list()

    for product in products:
        if not hasattr(product, "category"):
            product.category = "Uncategorized"
        if not hasattr(product, "subcategory"):
            product.subcategory = []
        await product.save()