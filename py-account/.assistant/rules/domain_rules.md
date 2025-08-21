# Domain Rules

## Base Model Rules
1. All domain models must inherit from BaseModel
2. Every entity must have:
   - UUID identifier
   - Creation timestamp (UTC)
   - Update timestamp (UTC)
   - Version UUID for optimistic locking
   - Soft delete capability

## User Domain Rules
1. Email and hashed password are required
2. Email must be unique
3. Password must be pre-hashed before reaching the domain model
4. Users can be soft-deleted but not hard-deleted
5. Version must be verified before updates

## Database Rules
1. Use PostgreSQL as the primary database
2. All database operations must be asynchronous
3. Use SQLAlchemy for ORM
4. Implement repository pattern for data access
5. Handle soft delete at repository level

## Concurrency Rules
1. Use optimistic locking for all updates
2. Version must be updated on every modification
3. Concurrent modifications must raise OptimisticLockException
4. All timestamps must be in UTC
