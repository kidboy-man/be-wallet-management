from datetime import datetime, timedelta, UTC
from functools import lru_cache
from jose import jwt

from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    """JWT settings for token generation and verification."""

    model_config = SettingsConfigDict(env_prefix="JWT_")
    
    # Token settings
    secret_key: str = "your-secret-key"  # TODO: Move to env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


@lru_cache
def get_token_settings() -> TokenSettings:
    """Get JWT token settings singleton."""
    return TokenSettings()


def create_access_token(data: dict) -> str:
    """Generate a new JWT access token.
    
    Args:
        data (dict): Data to encode in the token
        
    Returns:
        str: Generated JWT token
    """
    settings = get_token_settings()
    
    # Copy data to avoid modifying original
    payload = data.copy()
    
    # Set expiration
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp": expire})

    # Generate token
    encoded_jwt = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


from jose import JWTError, ExpiredSignatureError
from .exceptions import TokenError, TokenExpiredError, TokenInvalidError

def decode_token(token: str) -> dict:
    """Decode and verify a JWT token.
    
    Args:
        token (str): JWT token to decode
        
    Returns:
        dict: Decoded token data
        
    Raises:
        TokenExpiredError: If token has expired
        TokenInvalidError: If token is invalid
    """
    settings = get_token_settings()
    
    try:
        decoded_token = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return decoded_token
        
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
        
    except JWTError:
        raise TokenInvalidError("Invalid token")
