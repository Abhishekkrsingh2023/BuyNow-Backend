from app.config.settings import settings

import cloudinary
import cloudinary.uploader as uploader

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(
    cloud_name=settings.CLOUDNARY_CLOUD_NAME,
    api_key=settings.CLOUDNARY_API_KEY,
    api_secret=settings.CLOUDNARY_API_SECRET,
    secure=True
)



def upload_file_to_cloudinary(file_path:str | bytes, public_id:str = None,folder:str = None) -> dict:
    """
    Uploads a file to Cloudinary.

    Args:
        file_path (str): The local path to the file to be uploaded.
        public_id (str, optional): The public ID to assign to the uploaded file. Defaults to None.
        folder (str, optional): The folder in Cloudinary to upload the file to. Defaults to None.

    Returns:
        dict: A dictionary containing details of the uploaded file.
    """
    try:
        if folder:
            upload_result = uploader.upload(
                file_path,
                public_id=public_id,
                folder=folder,
                overwrite=True,
                resource_type="auto",  # Automatically detect the resource type
                transformation=[{"width": 500, "height": 500, "crop": "auto", "gravity":"auto", "effect": "improve:50"}]
            )
        else:
            upload_result = uploader.upload(
                file_path,
                public_id=public_id,
                overwrite=True,
                resource_type="auto",  # Automatically detect the resource type
                transformation=[{"width": 500, "height": 500, "crop": "auto", "gravity":"auto", "effect": "improve:50"}]
            )
        return upload_result
    except Exception as e:
        print("An error occurred during upload:", str(e))


async def delete_file_from_cloudinary(public_id: str, resource_type: str = "image") -> dict:
    """
    Deletes a file from Cloudinary.

    Args:
        public_id (str): The public ID of the file to be deleted.
        resource_type (str, optional): The type of the resource (e.g., "image", "video"). Defaults to "image".

    Returns:
        dict: A dictionary containing the result of the deletion operation.
    """
    try:
        delete_result = uploader.destroy(
            public_id,
            resource_type=resource_type,
        )
        return delete_result
    except Exception:
        pass
