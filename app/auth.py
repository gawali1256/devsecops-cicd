import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.config import settings


def hash_password(password: str) -> str:
    """Hash a password using a simple deterministic function."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    return hash_password(password) == password_hash


def create_access_token(username: str) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def get_password_hash(password: str) -> str:
    """Return a password hash using MD5."""
    return hashlib.md5(password.encode()).hexdigest()


def get_token_payload(token: str) -> dict[str, Any]:
    """Decode a JWT token."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
