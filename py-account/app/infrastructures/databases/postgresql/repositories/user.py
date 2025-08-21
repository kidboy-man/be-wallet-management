from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.interfaces.user import UserRepository
from app.repository.models.user import User
from app.infrastructures.databases.postgresql.models.user import UserModel

class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        db_user = UserModel.from_domain(user)
        self._session.add(db_user)
        await self._session.flush()
        await self._session.commit()
        return db_user.to_domain()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            uuid_id = UUID(user_id)
            stmt = select(UserModel).where(UserModel.id == uuid_id)
            result = await self._session.execute(stmt)
            db_user = result.scalar_one_or_none()
            return db_user.to_domain() if db_user else None
        except ValueError:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return db_user.to_domain() if db_user else None

    async def update(self, user: User) -> User:
        if not user.id:
            raise ValueError("User ID is required for update")
            
        # Fetch current state from database
        db_user = await self.get_by_id(str(user.id))
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")
        
        # Verify version to detect concurrent modifications
        user.verify_version(db_user.version)
        
        # Update version before saving
        user.update_version()
        
        updated_db_user = UserModel.from_domain(user)
        self._session.add(updated_db_user)
        await self._session.commit()
        return updated_db_user.to_domain()

    async def delete(self, user_id: str) -> bool:
        try:
            uuid_id = UUID(user_id)
            stmt = select(UserModel).where(UserModel.id == uuid_id)
            result = await self._session.execute(stmt)
            user_to_delete = result.scalar_one_or_none()
            
            if user_to_delete:
                await self._session.delete(user_to_delete)
                await self._session.commit()
                return True
            return False
        except ValueError:
            return False
