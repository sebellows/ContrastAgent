import hashlib
from urllib.parse import urlencode

def generate_gravatar_url(email: str, default: str = "robohash", size: int = 400) -> str:
    """
    Generate a Gravatar URL for the given email address.
    See: https://docs.gravatar.com/api/avatars/python/

    Args:
        email (str): The email address to generate the Gravatar URL for.
        default (str): The default image URL if the Gravatar is not found.
        size (int): The size of the Gravatar image.

    Returns:
        str: The Gravatar URL.
    """     
    # Encode the email to lowercase and then to bytes
    email_encoded = email.lower().encode('utf-8')
    
    # Generate the SHA256 hash of the email
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    
    # Construct the URL with encoded query parameters
    query_params = urlencode({'d': default, 's': str(size), 'r': 'x'})

    return f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"


DEFAULT_AVATAR_URL = generate_gravatar_url("john.warhammer@terra.com")
