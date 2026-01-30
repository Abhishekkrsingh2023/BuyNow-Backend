from fastapi import APIRouter, Depends,status


from app.dependencies.user_dependency import (
    login_user_dependency,
    get_current_user_dependency,
    update_user_dependency,
    get_user_logout_dependency,
)

router = APIRouter(
    prefix="/user",
    tags=["common"],
)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_profile(current_user= Depends(get_current_user_dependency)):
    return current_user

@router.post("/login",status_code=status.HTTP_200_OK)
async def login_user(user = Depends(login_user_dependency)):
    return user

@router.get("/logout",status_code=status.HTTP_201_CREATED)
async def logout_user(message=Depends(get_user_logout_dependency)):
    return message

@router.put("/update",status_code=status.HTTP_202_ACCEPTED,description="Update user details")
async def update_user(updated_user= Depends(update_user_dependency)):
    return updated_user

