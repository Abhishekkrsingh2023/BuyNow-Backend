import razorpay

from .settings import settings

def create_razorpay_client(key_id: str=settings.RAZORPAY_KEY_ID, key_secret: str=settings.RAZORPAY_KEY_SECRET) -> razorpay.Client:
    """
    Create and return a Razorpay client instance.

    Args:
        key_id (str): The Razorpay key ID.
        key_secret (str): The Razorpay key secret.

    Returns:
        razorpay.Client: An instance of the Razorpay client.
    """
    client = razorpay.Client(auth=(key_id, key_secret))
    return client