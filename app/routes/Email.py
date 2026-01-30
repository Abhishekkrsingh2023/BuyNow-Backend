from fastapi import (
    APIRouter,
    Depends,
    status
)
from app.dependencies.message_dependency import send_message_dependency

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_email(message = Depends(send_message_dependency)):
    return message