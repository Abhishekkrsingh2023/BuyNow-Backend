from datetime import datetime, timezone

def get_current_timestamp():
    """
    get_current_timestamp

    **Description:** Returns the current UTC timestamp
    """
    return datetime.now(timezone.utc)