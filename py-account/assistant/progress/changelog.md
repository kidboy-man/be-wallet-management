# Project Changelog

## 2025-08-21
- Implemented soft delete functionality in BaseModel
- Added optimistic locking with UUID versioning
- Created comprehensive unit tests for both features

### Key Implementations

#### Soft Delete
```python
def soft_delete(self) -> None:
    self.deleted_at = datetime.now(timezone.utc)

def restore(self) -> None:
    self.deleted_at = None

@property
def is_deleted(self) -> bool:
    return self.deleted_at is not None
```

#### Optimistic Locking
```python
def update_version(self) -> None:
    self.version = uuid4()
    self.updated_at = datetime.now(timezone.utc)

def verify_version(self, stored_version: UUID) -> None:
    if self.version != stored_version:
        raise OptimisticLockException(
            f"Concurrent modification detected. Expected version {self.version}, "
            f"but found {stored_version}"
        )
```

## Next Steps
- Implement soft delete and optimistic locking in SQLAlchemy models
- Update repository layer to handle these features
- Add integration tests
