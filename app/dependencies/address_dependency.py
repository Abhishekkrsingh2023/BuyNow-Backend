from fastapi import Depends, HTTPException
from app.auth_dependency import authenticate_user

from app.schemas import (
    Address,
    Users,
    UpdateAddress
)
from beanie import BeanieObjectId

from app.utils import get_current_timestamp
from app.constants import USER_EXCLUDE_FIELDS



async def add_new_address_dependency(address:Address, payload:dict=Depends(authenticate_user)):
    """
    add_new_address_dependency
    
    :param address: Description: The Address schema containing the new address details.
    :type address: Address
    :param payload: Description: The decoded JWT payload containing user information.
    :type payload: dict
    """
    user_id = payload.get("id")

    user = await Users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the address already exists based on all fields except 'id' and 'isDefault'
    if len(user.address) >= 5:
        raise HTTPException(status_code=400, detail="Address limit reached. Cannot add more than 5 addresses.")
    
    for addr in user.address:
        if (addr.street == address.street and
            addr.city == address.city and
            addr.state == address.state and
            addr.zipCode == address.zipCode and
            addr.country == address.country):
            raise HTTPException(status_code=400, detail="Address already exists")

    if address.isDefault:
        for addr in user.address:
            addr.isDefault = False

    user.address.append(address)
    user.updatedAt = get_current_timestamp()
    await user.save()

    user_response:dict = user.model_dump(exclude=USER_EXCLUDE_FIELDS)
    user_response["id"] = str(user.id)

    return {"success": True, "user": user_response}


async def update_address_dependency(
    address: UpdateAddress,
    payload: dict = Depends(authenticate_user)
):
    user_id = BeanieObjectId(payload["id"])

    update_data = address.model_dump(exclude_unset=True)
    address_id = update_data.pop("id")

    # If no other fields provided → nothing to update
    if len(update_data) == 0:
        raise HTTPException(400, "No fields to update")
    


    # Case 1: Updating 'isDefault' to True
    if update_data.get("isDefault") is True:
        result = await Users.find_one(Users.id == user_id).update(
            {
                "$set": {
                    # unset default for all addresses
                    "address.$[].isDefault": False,
                    # update only the matched address
                    **{f"address.$[elem].{k}": v for k, v in update_data.items()}
                }
            },
            array_filters=[{"elem.id": address_id}],
        )

    else:
        # Case 2: Regular partial update (no default change)
        result = await Users.find_one(Users.id == user_id).update(
            {
                "$set": {
                    # update only matched address fields
                    **{f"address.$[elem].{k}": v for k, v in update_data.items()}
                }
            },
            array_filters=[{"elem.id": address_id}],
        )

    if result.matched_count == 0:
        raise HTTPException(404, "Address not found")

    # Fetch updated user
    updated_user = await Users.get(user_id)

    user_response = updated_user.model_dump(exclude=USER_EXCLUDE_FIELDS)
    user_response["id"] = str(updated_user.id)

    return {"success": True, "user": user_response}

async def delete_address_dependency(address_id:str, payload:dict=Depends(authenticate_user)):
    """
    delete_address_dependency
    
    :param address_id: Description: The ID of the address to be deleted.
    :type address_id: str
    :param payload: Description: The decoded JWT payload containing user information.
    :type payload: dict
    """
    user_id = BeanieObjectId(payload.get("id"))

    result = await Users.find_one(Users.id == user_id).update(
        {
            "$pull": {
                "address": {"id": address_id}
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(404, "Address not found")

    return {"success": True, "message": "Address deleted successfully"}
