from unittest.mock import MagicMock
from app.services.auth_service import register_user, authenticate_user
from app.models.user import User
from app.core.auth_cache import user_cache, role_cache

def setup_function():
    user_cache.table = [[] for _ in range(user_cache.capacity)]
    role_cache.table = [[] for _ in range(role_cache.capacity)]
    
def test_register_user_populates_cache():
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    new_user = register_user(
        db=db,
        email="test@example.com",
        password="securepassword",
        username="testuser",
        role="farmer",
        location="Farmville",
        phone_number="1234567890"
    )

    cached_user = user_cache.get("test@example.com")
    cached_role = role_cache.get("test@example.com")
    
    assert cached_user is not None
    assert cached_user.email == "test@example.com"
    assert cached_role == "farmer"
    
def test_authenticate_user_uses_cache():
    db = MagicMock()
    fake_user = User(
        email="cached@example.com",
        hashed_password="hashedpw",
        username="cacheduser",
        role="buyer"
    )
    
    user_cache.put("cached@example.com", fake_user)
    role_cache.put("cached@example.com", "buyer")

    db.query().filter().first.side_effect = Exception("DB should not be queried")

    token = authenticate_user(db, "cached@example.com", "hashedpw")
    
    assert token is not None