"""Authentication related schemas."""
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.helpers.password import validate_password_complexity
from app.helpers.email import validate_email_format

class RegisterRequest(BaseModel):
    """Register request schema."""
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        is_valid, error = validate_password_complexity(password)
        if not is_valid:
            raise ValueError(error)
        return password
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, email: str) -> str:
        is_valid, error = validate_email_format(email)
        if not is_valid:
            raise ValueError(error)
        return email

class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"

class RegisterResponse(BaseModel):
    """Register response schema."""
    id: str
    email: str
    is_active: bool
    token: TokenResponse
