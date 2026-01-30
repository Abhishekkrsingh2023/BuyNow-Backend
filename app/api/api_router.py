from app.routes.user import router as user_router
from app.routes.common import router as common_router
from app.routes.seller import router as seller_router
from app.routes.products import router as product_router
from app.routes.admin import router as admin_router
from app.routes.payment import router as payment_router


from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(common_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(seller_router)
api_router.include_router(admin_router)
api_router.include_router(payment_router)