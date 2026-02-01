from fastapi import APIRouter, Depends,status

from app.dependencies.address_dependency import (
    add_new_address_dependency,
    update_address_dependency,
    delete_address_dependency,
)
    

router = APIRouter(
    prefix="/address",
    tags=["address"],
)

@router.post("/add-address",status_code=status.HTTP_201_CREATED)
async def add_address(message = Depends(add_new_address_dependency)):
    return message

@router.put("/update-address",status_code=status.HTTP_200_OK)
async def update_address(message = Depends(update_address_dependency)):
    return message

@router.delete("/delete-address",status_code=status.HTTP_200_OK)
async def delete_address(message = Depends(delete_address_dependency)):
    return message