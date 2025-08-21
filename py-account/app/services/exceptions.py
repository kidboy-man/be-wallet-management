"""Service layer exceptions."""

class ServiceError(Exception):
    """Base exception for service layer errors."""
    pass

class EmailAlreadyExistsError(ServiceError):
    """Raised when attempting to register with an existing email."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} is already registered")
