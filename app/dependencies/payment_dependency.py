import uuid

from beanie import BeanieObjectId
from fastapi import Depends, HTTPException, status

from app.config.payment_gateway import create_razorpay_client

from app.schemas import (
    OrderSchema,
    Products,
    Orders,
    PaymentVerificationSchema
)

from app.dependencies.user_dependency import get_current_user_dependency


async def create_order_details(order: OrderSchema, user_from_db=Depends(get_current_user_dependency)):
    """
    Docstring for create_order_details
    
    :param order: Description: The order details provided by the user.
    :type order: OrderSchema
    :param user_from_db: Description: The current authenticated user details.
    :type user_from_db: dict
    """
    razorpay_client = create_razorpay_client()
    order_data = order.model_dump(exclude_unset=True)

    user = user_from_db["user"]
    product_id = order_data['product_id']

    # Product matching with database
    product = await Products.get(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    quantity = order_data['quantity']
    amount = product.sellingPrice * quantity * 100  # Paise to Rupees conversion
    currency = "INR"
    receipt = f"BUYNOW_{str(uuid.uuid4())[:8]}"

    order_details ={
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "partial_payment": False,
        "notes": {
            "product_id": f"{product_id}",
            "product_name": f"{product.name}",
            "user_id": user["id"]
        }
    }
    try:
        # Create order in Razorpay
        razorpay_order = razorpay_client.order.create(order_details)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order with payment gateway"
        )
    
    address = order.address.model_dump()
    
    new_order = Orders(
        userId=BeanieObjectId(user["id"]),
        razorpay_order_id=razorpay_order['id'],
        receipt=receipt,  
        product_name=product.name,
        product_id=str(product_id),
        quantity=quantity,
        delivery_address=address,
        subTotalAmt=amount / 100,
        totalAmt=amount / 100,
    )

    await new_order.insert()
    return {"success": True, "order": razorpay_order}
    

async def verify_payment_signature(data: PaymentVerificationSchema):
    """
    Docstring for verify_payment_signature
    
    :param data: Description: The payment verification details provided by the user.
    :type data: PaymentVerificationSchema
    """
    razorpay_client = create_razorpay_client()
    verify_details = {
        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id,
        "razorpay_signature": data.razorpay_signature
    }
    # print("Verification details:", verify_details)  # Debugging line
    try:
        # Razorpay will raise SignatureVerificationError if invalid
        razorpay_client.utility.verify_payment_signature(verify_details)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment signature verification failed."
        )
    # if verified 
    await Orders.find_one(Orders.razorpay_order_id == data.razorpay_order_id).update({
        "$set": {
                "payment_status": "completed",
                "payment_id": data.razorpay_payment_id
            }
        })
    return {"success": True, "orderId": data.razorpay_order_id}

