from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import datetime

from beanie import (
    Document, 
    Indexed, 
    BeanieObjectId,
)

from app.utils import get_current_timestamp



class Users(Document):
    firstName: Annotated[str, Field(..., min_length=1, max_length=50)]
    lastName: Annotated[str, Field(..., min_length=1, max_length=50)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: Annotated[str, Field(..., min_length=8)]

    contactNo: Annotated[Optional[str], Field(default=None, min_length=7, max_length=15, alias="contactNumber")]
    role: Annotated[str, Field(default="user", alias="role")]

    avatarUrl: Annotated[Optional[str], Field(default=None, alias="avatarUrl")]
    avatarId: Annotated[Optional[str], Field(default=None, alias="avatarId")]
    isActive: Annotated[bool, Field(default=True, alias="isActive")]
    isVerified: Annotated[bool, Field(default=False, alias="isVerified")]
    verificationCode: Annotated[Optional[str], Field(default=None, alias="verificationCode")]

    cartId: Annotated[Optional[BeanieObjectId], Field(default=None, alias="cartId")]
    addressId: Annotated[Optional[BeanieObjectId], Field(default=None, alias="addressId")]

    createdAt: Annotated[datetime, Field(default_factory=get_current_timestamp)]
    updatedAt: Annotated[datetime, Field(default_factory=get_current_timestamp)]

    class Settings:
        name = "users"
    


class CreateUser(BaseModel):
    firstName: Annotated[str, Field(..., min_length=1, max_length=50, alias="firstName")]
    lastName: Annotated[str, Field(..., min_length=1, max_length=50, alias="lastName")]
    email: Annotated[EmailStr, Field(..., alias="email")]
    password: Annotated[str, Field(..., min_length=8)]
    contactNumber: Annotated[Optional[str], Field(default=None, min_length=7, max_length=15, alias="contactNumber")]


class UpdateUser(BaseModel):
    firstName: Annotated[Optional[str], Field(default=None, min_length=1, max_length=50, alias="firstName")]
    lastName: Annotated[Optional[str], Field(default=None, min_length=1, max_length=50, alias="lastName")]
    contactNumber: Annotated[Optional[str], Field(default=None, min_length=7, max_length=15, alias="contactNumber")]
    email: Annotated[Optional[EmailStr], Field(default=None, alias="email")]
    password: Annotated[Optional[str], Field(default=None, min_length=8)]
