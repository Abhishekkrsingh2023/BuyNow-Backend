import uuid

from beanie import (
    Document,
    BeanieObjectId,
    Indexed
)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils import get_current_timestamp



class Orders(Document):

    userId: Indexed(BeanieObjectId)  
    razorpay_order_id: Indexed(str, unique=True)
    reciept: Indexed(str) 

    payment_id: Optional[Indexed(str)] = None

    product_name: str
    product_id: str
    quantity: int

    delivery_address: dict

    subTotalAmt: float
    totalAmt: float

    delivery_status: str = "pending"
    payment_status: str = "pending"  

    createdAt: datetime = Field(default_factory=get_current_timestamp)
    updatedAt: datetime = Field(default_factory=get_current_timestamp)

    class Settings:
        name = "orders"

class Address(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    street: Optional[str] = Field(None)
    city: str = Field(...)
    state: str = Field(...)
    country: str = Field(...)
    zip_code: str = Field(...)
    is_default: bool = Field(default=False)


class OrderSchema(BaseModel):
    product_id: str
    amount: float | None = None
    quantity: int
    address: Address


class PaymentVerificationSchema(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str