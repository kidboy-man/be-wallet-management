from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from .base import BaseModel

class User(BaseModel):
    """User domain model.
    
    Attributes:
        email: User's email address
        hashed_password: Pre-hashed password
        is_active: Whether the user account is active
    """
    def __init__(
        self,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        id: Optional[UUID] = None,
        version: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ) -> None:
        super().__init__(
            id=id,
            version=version,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password are required")
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active

    @classmethod
    def create(cls, *, email: str, hashed_password: str) -> "User":
        """Create a new user.
        
        Args:
            email: User's email address
            hashed_password: Pre-hashed password
            
        Returns:
            User: New user instance with initial version
            
        Raises:
            ValueError: If email or hashed_password is empty
        """
        return cls(
            email=email,
            hashed_password=hashed_password,
            version=uuid4()
        )
