# Project Architecture

## Directory Structure
```
app/
├── infrastructures/
│   └── databases/
│       └── postgresql/
│           ├── models/
│           │   └── user.py
│           └── repositories/
│               └── user.py
└── repository/
    ├── interfaces/
    │   └── user.py
    └── models/
        ├── base.py
        └── user.py
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

## Technology Stack
- Python 3.12
- SQLAlchemy (async)
- PostgreSQL
- Poetry for dependency management
