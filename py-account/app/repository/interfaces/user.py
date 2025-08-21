from typing import Protocol, Optional
from ..models.user import User

class UserRepository(Protocol):
    async def create(self, user: User) -> User:
        """Create a new user"""
        ...

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        ...

    async def update(self, user: User) -> User:
        """Update user"""
        ...

    async def delete(self, user_id: str) -> bool:
        """Delete user"""
        ...
