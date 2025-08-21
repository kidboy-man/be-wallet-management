import pytest
from datetime import datetime
from uuid import UUID

from app.repository.models.user import User

def test_user_initialization():
    # Test basic initialization
    user = User(email="test@example.com", hashed_password="hashed123")
    assert isinstance(user.id, UUID)
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is None
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed123"
    assert user.is_active is True

def test_user_initialization_with_optional_params():
    test_id = UUID('12345678-1234-5678-1234-567812345678')
    test_date = datetime(2024, 1, 1)
    
    user = User(
        email="test@example.com",
        hashed_password="hashed123",
        is_active=False,
        id=test_id,
        created_at=test_date,
        updated_at=test_date
    )
    
    assert user.id == test_id
    assert user.created_at == test_date
    assert user.updated_at == test_date
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed123"
    assert user.is_active is False

def test_user_create_factory_method():
    user = User.create(
        email="test@example.com",
        hashed_password="hashed123"
    )
    assert isinstance(user.id, UUID)
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is None
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed123"
    assert user.is_active is True

def test_user_validation():
    with pytest.raises(ValueError):
        User(email="", hashed_password="hashed123")
    
    with pytest.raises(ValueError):
        User(email="test@example.com", hashed_password="")

    with pytest.raises(ValueError):
        User.create(email="", hashed_password="hashed123")
    
    with pytest.raises(ValueError):
        User.create(email="test@example.com", hashed_password="")
