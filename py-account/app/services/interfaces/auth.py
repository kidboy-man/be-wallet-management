"""Auth service interface."""
from typing import Protocol

from app.schemas.auth import RegisterRequest, RegisterResponse

class AuthService(Protocol):
    """Interface for authentication service."""
    
    async def register(self, request: RegisterRequest) -> RegisterResponse:
        """Register a new user.
        
        Args:
            request: Registration request containing email and password
            
        Returns:
            RegisterResponse with user info and access token
            
        Raises:
            ValueError: If email already exists
        """
        ...
