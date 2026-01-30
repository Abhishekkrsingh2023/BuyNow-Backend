from fastapi import Depends, HTTPException, Request,status
from app.core.security import verify_access_token

async def get_cookies(request: Request):
    """
    Retrieve access and refresh tokens from cookies.
    
    :param request: Description
    :type request: Request
    :return: tokens
    :rtype: dict
    """
    access = request.cookies.get("access_token")
    refresh = request.cookies.get("refresh_token")

    if not access:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing access token")

    return {"access_token": access, "refresh_token": refresh}

async def authenticate_user(cookies: dict = Depends(get_cookies))-> dict:
    """
    Docstring for authenticate_user
    
    :param cookies: Description
    :type cookies: dict
    :return: payload
    :rtype: dict
    """
    token = cookies["access_token"]

    payload = await verify_access_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    return payload