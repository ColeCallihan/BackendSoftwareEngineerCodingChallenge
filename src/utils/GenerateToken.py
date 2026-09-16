import string
import secrets

def generate_token(length: int=16):
    # Define Valid Characters
    alphabet = string.ascii_letters + string.digits
    
    # Securely choose random characters from the valid
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return token
