import pytest
from app.core.auth import create_access_token, verify_token

def test_jwt_token_creation():
    """Test JWT token creation"""
    data = {"sub": "test-user-id"}
    token = create_access_token(data)
    assert token is not None
    assert isinstance(token, str)

def test_jwt_token_verification():
    """Test JWT token verification"""
    data = {"sub": "test-user-id"}
    token = create_access_token(data)
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test-user-id"

def test_jwt_token_invalid():
    """Test invalid token verification"""
    payload = verify_token("invalid-token")
    assert payload is None

