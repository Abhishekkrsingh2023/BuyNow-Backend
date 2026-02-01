
import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field


class Address(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: str(uuid.uuid4()))]
    street: Annotated[str, Field(..., min_length=1, max_length=100)]
    city: Annotated[str, Field(..., min_length=1, max_length=50)]
    state: Annotated[str, Field(..., min_length=1, max_length=50)]
    zipCode: Annotated[str, Field(..., min_length=4, max_length=10)]
    country: Annotated[str, Field(..., min_length=1, max_length=50)]
    isDefault: Annotated[bool, Field(default=False, alias="isDefault")]

class UpdateAddress(BaseModel):
    id: Annotated[str, Field(..., alias="id")]
    street: Annotated[Optional[str], Field(default=None, min_length=1, max_length=100)]
    city: Annotated[Optional[str], Field(default=None, min_length=1, max_length=50)]
    state: Annotated[Optional[str], Field(default=None, min_length=1, max_length=50)]
    zipCode: Annotated[Optional[str], Field(default=None, min_length=4, max_length=10)]
    country: Annotated[Optional[str], Field(default=None, min_length=1, max_length=50)]
    isDefault: Annotated[Optional[bool], Field(default=False, alias="isDefault")]