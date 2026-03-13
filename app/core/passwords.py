# app/core/passwords.py

import hashlib
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        if ":" in hashed_password:
            salt, stored_hash = hashed_password.split(":", 1)
            computed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
            return secrets.compare_digest(computed, stored_hash)
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False