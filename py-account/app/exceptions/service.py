"""Service layer exceptions."""
from typing import Any, Dict, Optional

from .base import AppException, ErrorLayer, ErrorSeverity


class ServiceException(AppException):
    """Base exception for service layer."""

    def __init__(
        self,
        message: str,
        http_status: int,
        severity: ErrorSeverity,
        sequence: int,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize service exception."""
        super().__init__(message, http_status, severity, ErrorLayer.SERVICE, sequence, details)


class UserAlreadyExistsError(ServiceException):
    """Raised when attempting to register a user that already exists."""

    def __init__(self, email: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize user already exists error."""
        super().__init__(
            message=f"User with email {email} already exists",
            http_status=409,  # Conflict
            severity=ErrorSeverity.EXPECTED,  # Expected in normal flow
            sequence=1,
            details=details
        )


class InvalidCredentialsError(ServiceException):
    """Raised when login credentials are invalid."""

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize invalid credentials error."""
        super().__init__(
            message="Invalid email or password",
            http_status=401,  # Unauthorized
            severity=ErrorSeverity.EXPECTED,  # Expected in normal flow
            sequence=2,
            details=details
        )
