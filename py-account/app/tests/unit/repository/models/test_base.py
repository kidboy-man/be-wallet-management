import pytest
from datetime import datetime
from uuid import UUID, uuid4

from app.repository.models.base import BaseModel, OptimisticLockException

def test_base_model_initialization():
    # Test default initialization
    model = BaseModel()
    assert isinstance(model.id, UUID)
    assert isinstance(model.created_at, datetime)
    assert model.updated_at is None
    assert model.deleted_at is None
    assert not model.is_deleted
    
    # Test initialization with provided values
    test_id = UUID('12345678-1234-5678-1234-567812345678')
    test_date = datetime(2024, 1, 1)
    
    model = BaseModel(
        id=test_id,
        created_at=test_date,
        updated_at=test_date,
        deleted_at=test_date
    )
    
    assert model.id == test_id
    assert model.created_at == test_date
    assert model.updated_at == test_date
    assert model.deleted_at == test_date
    assert model.is_deleted

def test_soft_delete_restore():
    model = BaseModel()
    assert not model.is_deleted
    assert model.deleted_at is None
    
    # Test soft delete
    model.soft_delete()
    assert model.is_deleted
    assert isinstance(model.deleted_at, datetime)
    
    # Test restore
    model.restore()
    assert not model.is_deleted
    assert model.deleted_at is None

def test_optimistic_locking():
    # Initialize model
    initial_version = uuid4()
    model = BaseModel(version=initial_version)
    assert model.version == initial_version
    
    # Test version update
    old_version = model.version
    model.update_version()
    assert model.version != old_version
    assert isinstance(model.version, UUID)
    assert isinstance(model.updated_at, datetime)
    
    # Test version verification - success
    model.verify_version(model.version)  # Should not raise
    
    # Test version verification - failure
    with pytest.raises(OptimisticLockException):
        model.verify_version(uuid4())
