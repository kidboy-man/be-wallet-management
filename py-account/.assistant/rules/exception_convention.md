# Exception Handling Conventions

## Error Code Structure

Error codes follow the format: `{http_status}{severity}{layer}{sequence}`

Example: `40399010001` breaks down as:
- `403`: HTTP status code
- `99`: Severity level
- `01`: Layer identifier
- `001`: Sequence number

### HTTP Status Codes
Use standard HTTP status codes that best match the error:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `422`: Unprocessable Entity
- `500`: Internal Server Error
- `503`: Service Unavailable

### Severity Levels
- `00`: CRITICAL - System failures, data corruption
- `10`: HIGH - Security issues, data integrity
- `20`: MEDIUM - Business rule violations
- `30`: LOW - Validation errors, recoverable issues
- `99`: EXPECTED - Normal business flow errors

### Layer Identifiers (01-99)
- `01`: Infrastructure - DB, external services, JWT
- `02`: Repository - Data access layer
- `03`: Domain - Core business logic
- `04`: Service - Application services
- `05`: Controller - API endpoints
- `06`: Presentation - UI/Presentation layer

### Sequence Numbers (001-999)
- Three-digit incremental number within each layer
- Start from 001 and increment by 1
- Group related errors with close sequence numbers

## Exception Class Structure

### Base Exception
All custom exceptions inherit from `AppException` which provides:
- Error code generation
- Standard error message formatting
- Optional details dictionary

### Layer Exceptions
Each layer has its base exception class:
```python
class LayerException(AppException):
    """Base exception for specific layer."""
    _layer = ErrorLayer.LAYER_NAME  # Define layer once for all derived exceptions
```

### Specific Exceptions
Each specific exception should:
1. Inherit from its layer's base exception
2. Define all error properties as class variables
3. Only allow `details` parameter in __init__

Example:
```python
class SpecificError(LayerException):
    """Clear description of when this error occurs."""
    _message = "Clear error message"
    _http_status = 4XX  # Appropriate HTTP status
    _severity = ErrorSeverity.LEVEL
    _sequence = N  # Unique in this layer

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=self._message,
            http_status=self._http_status,
            severity=self._severity,
            sequence=self._sequence,
            details=details
        )
```

## Usage Guidelines

### When to Create New Exceptions
1. Create a new exception when:
   - Error needs different handling
   - Error represents a distinct failure mode
   - Error requires different HTTP status or severity

2. Reuse existing exceptions when:
   - Error represents same failure mode
   - Error would have same handling
   - Only message details differ

### Error Details
- Use `details` for variable information
- Keep messages generic in class definition
- Add specific details when raising

Example:
```python
raise UserNotFoundError(details={"user_id": "123"})
```

### Documentation
Each exception class must have:
1. Clear docstring explaining when it occurs
2. Comment explaining HTTP status choice if not obvious
3. Comment explaining severity level if not obvious
4. Comment showing error code format
