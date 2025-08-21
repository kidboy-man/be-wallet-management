class TokenError(Exception):
    """Base exception for token-related errors."""
    pass


class TokenExpiredError(TokenError):
    """Exception raised when token has expired."""
    pass


class TokenInvalidError(TokenError):
    """Exception raised when token is invalid."""
    pass
