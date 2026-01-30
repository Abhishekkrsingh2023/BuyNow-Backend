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


# print(config)

# # Log the configuration
# # ==============================
# print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

def upload_file_to_cloudinary(file_path:str, public_id:str = None) -> dict:
    """
    Uploads a file to Cloudinary.

    Args:
        file_path (str): The local path to the file to be uploaded.
        public_id (str, optional): The public ID to assign to the uploaded file. Defaults to None.

    Returns:
        dict: A dictionary containing details of the uploaded file.
    """
    try:
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
    except Exception as e:
        print("An error occurred during deletion:", str(e))

async def upload_many_files_to_cloudinary(file_paths: list) -> list:
    """
    Uploads multiple files to Cloudinary.

    Args:
        file_paths (list): A list of local paths to the files to be uploaded.

    Returns:
        list: A list of dictionaries containing details of the uploaded files.
    """
    upload_results = []
    for file_path in file_paths:
        try:
            upload_result = cloudinary.uploader.upload(
                file_path,
                overwrite=True,
                resource_type="auto",  # Automatically detect the resource type
                transformation=[{"width": 400, "height": 400, "crop": "auto", "gravity":"auto", "effect": "improve:50"}]
            )
            upload_results.append(upload_result)
        except Exception as e:
            print(f"An error occurred during upload of {file_path}:", str(e))
            raise Exception(f"Upload failed for {file_path}: {str(e)}")
    return upload_results

async def delete_many_files_from_cloudinary(public_ids: list, resource_type: str = "image") -> dict:
    """
    Deletes multiple files from Cloudinary.

    Args:
        public_ids (list): A list of public IDs of the files to be deleted.
        resource_type (str, optional): The type of the resources (e.g., "image", "video"). Defaults to "image".

    Returns:
        dict: A dictionary containing the results of the deletion operations.
    """
    deleted_results = []
    for public_id in public_ids:
        try:
            delete_result = uploader.destroy(
                public_id,
                resource_type=resource_type,    
                transformation=[{"width": 400, "height": 400, "crop": "auto", "gravity":"auto", "effect": "improve:50"}]
            )
            deleted_results.append(delete_result)
        except Exception as e:
            print(f"An error occurred during deletion of {public_id}:", str(e))
            raise Exception(f"Deletion failed for {public_id}: {str(e)}")
        
    return deleted_results