# Code Conventions

## Pydantic Schema Rules
1. Always use Pydantic v2 conventions:
   - Use `@field_validator` instead of deprecated `@validator`
   - Include `@classmethod` with field validators
   - Use `EmailStr` for email field validation
   - Define clear validation error messages

2. Schema Naming:
   - Request DTOs: Suffix with `Request` (e.g., `RegisterRequest`)
   - Response DTOs: Suffix with `Response` (e.g., `RegisterResponse`)
   - Nested DTOs: Use descriptive names (e.g., `TokenResponse`)

3. Schema Organization:
   - Group related schemas in same file (e.g., `auth.py` for auth-related schemas)
   - Keep schemas flat when possible
   - Use nested schemas for reusable structures

## Helper Functions
1. Input Validation:
   - Return tuple[bool, Optional[str]] for validation results
   - First value: validation status (True/False)
   - Second value: error message if validation fails, None if success
   - Clear, specific error messages for each validation rule

2. Function Naming:
   - Validation functions: prefix with `validate_` (e.g., `validate_password_complexity`)
   - Utility functions: use verb_noun format (e.g., `hash_password`)

3. Documentation:
   - Include docstrings with Args, Returns, and Raises sections
   - Document all validation rules in docstring
   - Include usage examples for complex functions

## Type Hints
1. Always use type hints:
   - Use Optional[] for nullable values
   - Use proper return type annotations
   - Import types from typing module
   - Use concrete types when possible

## Error Handling
1. Validation Errors:
   - Raise ValueError with clear messages
   - Use custom exceptions for specific cases
   - Include context in error messages

2. Error Messages:
   - Be specific about what failed
   - Include requirements in message
   - User-friendly wording

## Code Organization
1. Related Functionality:
   - Group related validators together
   - Keep validation logic in helpers
   - Use schema validators for input validation
   - Keep business logic in services

2. Imports:
   - Group imports by type (standard lib, third party, local)
   - Use specific imports over module imports
   - Import validators from pydantic directly
