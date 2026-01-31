from fastapi import Response


def set_cookie(response: Response, key: str, value: str, max_age: int=3600): # default 1hr
    """
    Docstring for set_cookie
    
    :param response: The response object where the cookie will be set
    :type response: Response
    :param key: The key/name of the cookie
    :type key: str
    :param value: The value of the cookie
    :type value: str
    :param max_age: The maximum age of the cookie in seconds
    :type max_age: int
    """
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        max_age=max_age,
        expires=max_age,
        path="/",
        secure=True,
        samesite="none",
    )

def delete_cookie(response: Response, key: str):
    """
    Docstring for delete_cookie
    
    :param response: The response object where the cookie will be deleted
    :type response: Response
    :param key: The key/name of the cookie to be deleted
    :type key: str
    """
    response.delete_cookie(
        key=key,
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )