from pydantic import BaseModel, EmailStr, Field



class Login(BaseModel):
    email: EmailStr = Field(..., alias="email")
    password: str = Field(..., alias="password")


class OTPVerification(BaseModel):
    email: EmailStr = Field(..., alias="email")
    otp: str = Field(..., alias="otp")