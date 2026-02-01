from app.routes import (
    common_router,
    user_router,
    address_router,
    seller_router,
    product_router,
    admin_router,
    payment_router,
    email_router,
)


from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(common_router)
api_router.include_router(user_router)
api_router.include_router(address_router)
api_router.include_router(seller_router)
api_router.include_router(product_router)
api_router.include_router(admin_router)
api_router.include_router(payment_router)
api_router.include_router(email_router)