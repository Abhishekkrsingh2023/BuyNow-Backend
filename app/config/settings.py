from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Define settings model
class Settings(BaseSettings):
    
    # Database settings
    MONGO_URL: str = Field(..., env="MONGO_URL")
    DATABASE_NAME: str = Field("ecommerce_db", env="DATABASE_NAME")
    JWT_ACCESS_SECRET_KEY: str = Field(..., env="JWT_ACCESS_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = Field(..., env="JWT_REFRESH_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Cloudinary settings
    CLOUDNARY_CLOUD_NAME: str = Field(..., env="CLOUDNARY_CLOUD_NAME")
    CLOUDNARY_API_KEY: str = Field(..., env="CLOUDNARY_API_KEY")
    CLOUDNARY_API_SECRET: str = Field(..., env="CLOUDNARY_API_SECRET")

    # gmail settings
    SENDERS_EMAIL: str = Field(..., env="SENDERS_EMAIL")
    GMAIL_PASSWORD: str = Field(..., env="GMAIL_PASSWORD")

    # Razorpay settings
    RAZORPAY_KEY_ID: str = Field(..., env="RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: str = Field(..., env="RAZORPAY_KEY_SECRET")

    # Configuration for loading .env
    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8")

# Load settings
try:
    settings = Settings()
except Exception as e:
    raise SystemExit(f"Error loading settings: {e}")
