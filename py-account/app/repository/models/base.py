from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

class OptimisticLockException(Exception):
    """Raised when a concurrent modification is detected."""
    pass

class BaseModel:
    """Base model for all domain models with soft delete support and optimistic locking."""
    def __init__(
        self,
        id: Optional[UUID] = None,
        version: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ) -> None:
        self.id = id or uuid4()
        self.version = version or uuid4()
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def soft_delete(self) -> None:
        """Mark the record as deleted by setting deleted_at timestamp."""
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """Restore a soft-deleted record by clearing deleted_at."""
        self.deleted_at = None

    def update_version(self) -> None:
        """Update the version for optimistic locking."""
        self.version = uuid4()
        self.updated_at = datetime.now(timezone.utc)

    def verify_version(self, stored_version: UUID) -> None:
        """Verify that the version matches the stored version.
        
        Args:
            stored_version: The version from the database
            
        Raises:
            OptimisticLockException: If versions don't match, indicating concurrent modification
        """
        if self.version != stored_version:
            raise OptimisticLockException(
                f"Concurrent modification detected. Expected version {self.version}, "
                f"but found {stored_version}"
            )

    @property
    def is_deleted(self) -> bool:
        """Check if the record is soft-deleted."""
        return self.deleted_at is not None
