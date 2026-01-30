from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    status
)

from contextlib import asynccontextmanager
from database.connection import client
from database.collections import admins_collection
from schemas.user_schema import CreateUser,Login
from utils.DateTimeUTC import get_current_utc_datetime
from core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await client.admin.command('ping')
    print("Database connection established.")
    # Initialize resources here
    yield
    print("Shutting down...")
    print("Closing database connection...")
    await client.close()
    # Cleanup resources here

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Health": "Ok!"}

@app.post("/admin/create-admin",status_code=status.HTTP_201_CREATED)
async def create_admin(admin_data: CreateUser):
    admin = admin_data.model_dump()

    is_admin = await admins_collection.find_one({"email": admin["email"]})
    if is_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists.")
    
    admin["password"] = hash_password(admin["password"])
    admin["is_admin"] = True
    admin["role"] = "admin"
    admin["created_at"] = admin["updated_at"] = get_current_utc_datetime()
    result = await admins_collection.insert_one(admin)

    return {"admin_id": str(result.inserted_id)}


@app.post("/admin/login",status_code=status.HTTP_200_OK)
async def admin_login(login:Login,response: Response):

    data = login.model_dump()

    admin = await admins_collection.find_one({"email": data["email"], "is_admin": True})
    if not admin or not verify_password(data["password"], admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(admin["_id"]), "role": "admin"})
    refresh_token = create_refresh_token({"sub": str(admin["_id"]), "role": "admin"})
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=1800,  # 30 minutes
        path="/",
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=1800,  # 30 minutes
        path="/",
    )
    admin["_id"] = str(admin["_id"])
    admin.pop("password", None)  # Remove password before returning

    return admin