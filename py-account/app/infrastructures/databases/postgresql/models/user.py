from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from app.infrastructures.databases.postgresql.connection import Base

if TYPE_CHECKING:
    from app.repository.models.user import User

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)  # type: ignore
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)  # type: ignore
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)  # type: ignore
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)  # type: ignore
    created_at: Mapped[datetime] = mapped_column(  # type: ignore
        DateTime(timezone=True), 
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(  # type: ignore
        DateTime(timezone=True), 
        nullable=True
    )

    def to_domain(self) -> "User":
        from app.repository.models.user import User
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, user: "User") -> "UserModel":
        return cls(
            id=user.id or uuid4(),
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at or datetime.utcnow(),
            updated_at=user.updated_at
        )
