"""Infrastructure layer exceptions.

This module contains all infrastructure-related exceptions including database,
external services, and authentication errors.
"""
from typing import Any, Dict, Optional

from .base import AppException, ErrorLayer, ErrorSeverity


class InfrastructureException(AppException):
    """Base exception for infrastructure layer.
    
    All infrastructure-specific exceptions should inherit from this class.
    Infrastructure layer handles external services, databases, and technical concerns.
    """
    _layer = ErrorLayer.INFRASTRUCTURE


class DatabaseConnectionError(InfrastructureException):
    """Raised when unable to establish a database connection.
    
    Error Code: 50300001001
    - 503: Service Unavailable
    - 00: Critical severity (system failure)
    - 01: Infrastructure layer
    - 001: First database-related error
    """
    _message = "Failed to connect to database"
    _http_status = 503  # Service Unavailable - Database is a critical service
    _severity = ErrorSeverity.CRITICAL  # System can't function without database
    _sequence = 1  # First database error

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize database connection error.
        
        Args:
            details: Optional additional error context (e.g., connection string, timeout)
        """
        super().__init__(
            message=self._message,
            http_status=self._http_status,
            severity=self._severity,
            sequence=self._sequence,
            details=details
        )


class DatabaseQueryError(InfrastructureException):
    """Raised when a database query fails to execute.
    
    Error Code: 50000001002
    - 500: Internal Server Error
    - 00: Critical severity
    - 01: Infrastructure layer
    - 002: Second database-related error
    """
    _message = "Failed to execute database query"
    _http_status = 500  # Internal Server Error - Query execution failure
    _severity = ErrorSeverity.CRITICAL
    _sequence = 2  # Second database error

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize database query error.
        
        Args:
            details: Optional error context (e.g., query, parameters, error message)
        """
        super().__init__(
            message=self._message,
            http_status=self._http_status,
            severity=self._severity,
            sequence=self._sequence,
            details=details
        )


class TokenExpiredError(InfrastructureException):
    """Raised when JWT token has expired.
    
    Error Code: 40199001003
    - 401: Unauthorized
    - 99: Expected severity (normal auth flow)
    - 01: Infrastructure layer
    - 003: Third error, first auth-related
    """
    _message = "Authentication token has expired"
    _http_status = 401  # Unauthorized - Client needs to reauthenticate
    _severity = ErrorSeverity.EXPECTED  # Normal part of auth flow
    _sequence = 3  # First auth error

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize token expired error.
        
        Args:
            details: Optional error context (e.g., token, expiry time)
        """
        super().__init__(
            message=self._message,
            http_status=self._http_status,
            severity=self._severity,
            sequence=self._sequence,
            details=details
        )


class TokenInvalidError(InfrastructureException):
    """Raised when JWT token is invalid (malformed, wrong signature, etc).
    
    Error Code: 40110001004
    - 401: Unauthorized
    - 10: High severity (potential security issue)
    - 01: Infrastructure layer
    - 004: Fourth error, second auth-related
    """
    _message = "Invalid authentication token"
    _http_status = 401  # Unauthorized - Invalid credentials
    _severity = ErrorSeverity.HIGH  # Security concern
    _sequence = 4  # Second auth error

    def __init__(self, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize token invalid error.
        
        Args:
            details: Optional error context (e.g., validation errors)
        """
        super().__init__(
            message=self._message,
            http_status=self._http_status,
            severity=self._severity,
            sequence=self._sequence,
            details=details
        )
