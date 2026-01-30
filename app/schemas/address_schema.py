
from beanie import (
    Document,
    Link, 
)
from pydantic import BaseModel, Field
from typing import Optional

from datetime import datetime
from app.utils import get_current_timestamp

from .user_schema import Users


class Address(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    street: Optional[str] = Field(None)
    city: str = Field(...)
    state: str = Field(...)
    country: str = Field(...)
    zip_code: str = Field(...)
    is_default: bool = Field(default=False)


class Addresses(Document):
    user: Link["Users"]
    addresses: list[Address] = Field(default_factory=list)

    createdAt: datetime = Field(default_factory=get_current_timestamp)
    updatedAt: datetime = Field(default_factory=get_current_timestamp)

    class Settings:
        name = "addresses"
    

