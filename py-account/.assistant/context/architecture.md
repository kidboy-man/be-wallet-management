# Project Architecture

## Directory Structure
```
py-account/
├── app/
│   ├── schemas/                  # Data Transfer Objects (DTOs)
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth-related schemas
│   │   └── user.py              # User-related schemas
│   │
│   ├── controllers/              # Input layer adapters
│   │   ├── __init__.py
│   │   ├── http/                # HTTP adapter
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   └── user.py
│   │   │   └── middlewares/
│   │   └── consumer/           # Event consumer adapter
│   │       └── __init__.py
│   │
│   ├── services/               # Pure business logic
│   │   ├── __init__.py
│   │   ├── interfaces/        # Service contracts
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   ├── auth.py           # Auth service implementation
│   │   ├── user.py          # User service implementation
│   │   └── exceptions.py
│   │
│   ├── repository/           # Data access contracts
│   │   ├── __init__.py
│   │   ├── interfaces/      # Repository contracts
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   ├── models/         # Domain entities
│   │   │   ├── user.py    # Pure domain models (no ORM!)
│   │   │   └── token.py
│   │   └── exceptions.py
│   │
│   ├── infrastructures/    # Technical implementations
│   │   ├── __init__.py
│   │   ├── databases/
│   │   │   ├── __init__.py
│   │   │   └── postgresql/
│   │   │       ├── __init__.py
│   │   │       ├── connection.py
│   │   │       ├── repositories/
│   │   │       │   ├── auth.py
│   │   │       │   └── user.py
│   │   │       ├── models/     # ORM models
│   │   │       └── alembic/    # Migrations for PostgreSQL
│   │   └── security/
│   │       ├── jwt.py
│   │       └── password.py
│   │
│   ├── config/            # Application configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   └── tests/            # Tests moved under app
│       ├── __init__.py
│       ├── conftest.py
│       ├── unit/
│       │   ├── services/
│       │   └── repository/
│       └── integration/
│           ├── controllers/
│           └── infrastructures/
│
└── deployment/
    └── docker/
        ├── Dockerfile
        └── docker-compose.yml
```

## Architectural Decisions

### 1. Hexagonal Architecture
- **Decision**: Use hexagonal (ports and adapters) architecture
- **Reasoning**: Clear separation between domain logic and external concerns
- **Implementation**: Domain models in repository/models, interfaces in repository/interfaces

### 2. Repository Pattern
- **Decision**: Use repository pattern for data access
- **Reasoning**: Abstract data persistence, easier testing and switching implementations
- **Implementation**: Interface in repository/interfaces, implementation in infrastructures/databases

### 3. Optimistic Locking
- **Decision**: Use UUID for version control
- **Reasoning**: Better conflict detection than timestamps, works well with distributed systems
- **Implementation**: Version field in BaseModel, verified in repository operations

### 4. Soft Delete
- **Decision**: Implement soft delete in base model
- **Reasoning**: Maintain data history, allow for recovery, support compliance requirements
- **Implementation**: deleted_at timestamp, is_deleted property

## Layer Explanations

### Controllers Layer (Input Adapters)
- HTTP controllers for REST API endpoints
- Event consumers for message queue processing
- Input validation and DTOs
- Route definitions and middleware

### Services Layer (Business Logic)
- Pure business logic implementation
- Service interfaces/contracts
- No infrastructure dependencies
- Business rules and validations

### Repository Layer (Data Access Contracts)
- Domain model definitions
- Repository interfaces
- Pure domain entities without ORM
- Domain-specific exceptions

### Infrastructure Layer (Technical Implementations)
- Database implementations (PostgreSQL)
- Security implementations (JWT, password hashing)
- External service integrations
- Technical concerns

### Configuration Layer
- Environment-specific settings
- Application configuration
- Feature flags

### Tests Layer
- Unit tests for business logic
- Integration tests for infrastructure
- Controller tests for HTTP endpoints
- Test fixtures and utilities

## Technology Stack
- Python 3.12
- SQLAlchemy (async)
- PostgreSQL
- Poetry for dependency management
