import pytest
from datetime import datetime, timedelta
from jose import jwt

from ....infrastructures.security.jwt import (
    create_access_token, 
    decode_token,
    get_token_settings,
)
from ....infrastructures.security.exceptions import TokenExpiredError, TokenInvalidError

def test_create_access_token():
    # Arrange
    data = {"sub": "test@example.com"}
    settings = get_token_settings()
    
    # Act
    token = create_access_token(data)
    
    # Assert
    decoded = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded

def test_decode_token():
    # Arrange
    settings = get_token_settings()
    payload = {"sub": "test@example.com"}
    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    # Act
    decoded = decode_token(token)
    
    # Assert
    assert decoded["sub"] == "test@example.com"

def test_decode_expired_token():
    # Arrange
    settings = get_token_settings()
    payload = {
        "sub": "test@example.com",
        "exp": datetime.utcnow() - timedelta(minutes=1)
    }
    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    # Act & Assert
    with pytest.raises(TokenExpiredError):
        decode_token(token)

def test_decode_invalid_token():
    # Arrange
    invalid_token = "invalid.token.here"
    
    # Act & Assert
    with pytest.raises(TokenInvalidError):
        decode_token(invalid_token)
