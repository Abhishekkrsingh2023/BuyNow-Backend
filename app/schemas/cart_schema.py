from pydantic import BaseModel,Field

from typing import Annotated, List
from datetime import datetime

from beanie import (
    Document, 
    Indexed,
    Link,
    BeanieObjectId
)

from .user_schema import Users
from app.utils import get_current_timestamp


class CartItem(BaseModel):
    productId: Annotated[BeanieObjectId, Field(..., alias="productId")]
    quantity: Annotated[int, Field(default=1, gt=0)]


class Carts(Document):
    user: Annotated[Link["Users"], Indexed(unique=True)]
    items: Annotated[List[CartItem], Field(default_factory=list)]

    createdAt: datetime = Field(default_factory=get_current_timestamp)
    updatedAt: datetime = Field(default_factory=get_current_timestamp)

    class Settings:
        name = "carts"
    
