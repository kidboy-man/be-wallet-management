"""Base exception module for the application."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


class ErrorSeverity(Enum):
    """Enum for error severity levels."""
    CRITICAL = "00"  # System failures, data corruption
    HIGH = "10"      # Security issues, data integrity
    MEDIUM = "20"    # Business rule violations
    LOW = "30"      # Validation errors, recoverable issues
    EXPECTED = "99"  # Normal business flow errors


class ErrorLayer(Enum):
    """Enum for application layers."""
    INFRASTRUCTURE = "01"  # DB, external services, JWT
    REPOSITORY = "02"      # Data access layer
    DOMAIN = "03"         # Core business logic
    SERVICE = "04"        # Application services
    CONTROLLER = "05"     # API endpoints
    PRESENTATION = "06"   # UI/Presentation layer


@dataclass
class ErrorCode:
    """Error code generator."""
    http_status: int
    severity: ErrorSeverity
    layer: ErrorLayer
    sequence: int

    def __str__(self) -> str:
        """Generate the error code string."""
        return f"{self.http_status}{self.severity.value}{self.layer.value}{str(self.sequence).zfill(3)}"


class AppException(Exception):
    """Base exception class for the application."""

    def __init__(
        self,
        message: str,
        http_status: int,
        severity: ErrorSeverity,
        layer: ErrorLayer,
        sequence: int,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: Human-readable error message
            http_status: HTTP status code
            severity: Error severity level
            layer: Application layer where the error occurred
            sequence: Error sequence number within the layer
            details: Additional error details (optional)
        """
        self.message = message
        self.code = str(ErrorCode(http_status, severity, layer, sequence))
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format.
        
        Returns:
            Dict containing error details
        """
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details
        }
