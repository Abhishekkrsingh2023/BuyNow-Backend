from fastapi import Depends, HTTPException, Request, status
from app.core import verify_access_token, verify_refresh_token

async def get_access_cookies(request: Request):
    """
    Retrieve access and refresh tokens from cookies.
    
    :param request: Description
    :type request: Request
    :return: tokens
    :rtype: dict
    """
    access = request.cookies.get("access_token")
    if not access:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing authentication cookies")

    return {"access_token": access}

async def get_refresh_cookie(request: Request):
    """
    Docstring for get_refresh_cookie
    
    :param request: extracts refresh token from cookies
    :type request: Request
    """
    refresh = request.cookies.get("refresh_token")
    if not refresh:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing refresh token")
    return {"refresh_token": refresh}


async def authenticate_user(cookies: dict = Depends(get_access_cookies))-> dict:
    """
    Docstring for authenticate_user
    
    :param cookies: gets the access token from cookies
    :type cookies: dict
    :return: payload
    :rtype: dict
    """
    access_token = cookies["access_token"]

    payload = await verify_access_token(access_token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    return payload


async def auth_refresh_token(token: dict = Depends(get_refresh_cookie)):
    """
    Docstring for auth_refresh_token
    
    :param token: gets the refresh token from cookies
    :type token: dict
    """
    refresh_token = token["refresh_token"]

    payload = await verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    return payload

