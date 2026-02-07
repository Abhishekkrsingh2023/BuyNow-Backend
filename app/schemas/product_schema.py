
from datetime import datetime
from pydantic import Field
from typing_extensions import Annotated

from beanie import (
    Document,
    Indexed, 
    Link,
)

from .user_schema import Users
from app.utils import get_current_timestamp


# class Products(Document):
#     sellerID: Annotated[Link["Users"], Indexed()]
#     name: str
#     description: str
#     sellingPrice: Annotated[float, Field(..., alias="sellingPrice", gt=0)]
#     mrp: Annotated[float, Field(..., alias="mrp", gt=0)]
#     quantity: int
#     in_stock: bool = True

#     imageUrl: list[dict] = Field(default_factory=list)
#     createdAt: datetime = Field(default_factory=get_current_timestamp)
#     updatedAt: datetime = Field(default_factory=get_current_timestamp)

#     class Settings:
#         name = "products"

class Products(Document):
    sellerID: Annotated[Link["Users"], Indexed()]
    name: str
    description: str
    sellingPrice: Annotated[float, Field(..., alias="sellingPrice", gt=0)]
    mrp: Annotated[float, Field(..., alias="mrp", gt=0)]
    quantity: int
    in_stock: bool = True

    category: str # eg: "Electronics", "Clothing", "Home Appliances", etc.
    subcategory: list[str] = Field(default_factory=list) # eg: For "Electronics" category, subcategories could be "Mobile Phones", "Laptops", "Cameras", etc.

    images: list[dict] = Field(default_factory=list)
    createdAt: datetime = Field(default_factory=get_current_timestamp)
    updatedAt: datetime = Field(default_factory=get_current_timestamp)

    class Settings:
        name = "products"