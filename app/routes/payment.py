from fastapi import APIRouter, Depends,status

from app.dependencies.payment_dependency import (
    create_order_details,
    verify_payment_signature,
)

router = APIRouter(
    prefix="/payment",
    tags=["payments"],
)

@router.post("/create-order", status_code=status.HTTP_201_CREATED)
async def create_payment_order(order_details=Depends(create_order_details)):
    return order_details

@router.post("/verify-payment", status_code=status.HTTP_200_OK)
async def verify_payment(verification_result=Depends(verify_payment_signature)):
    return verification_result
