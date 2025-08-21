"""Email validation utilities."""
import re
from typing import Optional

def validate_email_format(email: str) -> tuple[bool, Optional[str]]:
    """Validate email format.
    
    Args:
        email: The email to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, "Email is required"
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, None
