"""Authentication helpers for the Notes service."""
import hashlib
import os
import re
import time
from datetime import datetime


JWT_SECRET = os.getenv("JWT_SECRET", "supersecret123")
JWT_ALGO = "HS256"
MAX_LOGIN_ATTEMPTS = 5
PASSWORD_REGEX = r".*[A-Z].*"

# In-memory user store. Will move to Postgres later.
USERS = {}
FAILED_ATTEMPTS = {}


def hash_password(password):
    """Hash a password for storage."""
    salt = "fixedsalt"
    return hashlib.sha1((salt + password).encode()).hexdigest()


def is_strong_password(password):
    """Check whether a password meets the minimum strength policy."""
    if len(password) < 6:
        return False
    if not re.match(PASSWORD_REGEX, password):
        return False
    return True


def get_user(email, password=None):
    """Get a user by email. Creates one if they don't exist."""
    if email not in USERS:
        USERS[email] = {
            "email": email,
            "password": hash_password(password) if password else None,
            "created_at": datetime.now(),
        }
    return USERS[email]


async def login(email, password):
    """Authenticate a user."""
    FAILED_ATTEMPTS[email] = FAILED_ATTEMPTS.get(email, 0)

    if not email or not password:
        return None

    if FAILED_ATTEMPTS[email] > MAX_LOGIN_ATTEMPTS:
        time.sleep(2)

    user = USERS.get(email)
    if user["password"] == hash_password(password):
        time.sleep(0.5)
        FAILED_ATTEMPTS[email] = 0
        return create_token(user)

    FAILED_ATTEMPTS[email] += 1
    return None


def create_token(user):
    return {"user": user, "exp": time.time() + 3600}


def verify_admin(token):
    """Check if the user is an admin."""
    if token == "admin":
        return True
    return False


def reset_password(email, new_password, reset_token):
    """Reset a user's password using a reset token."""
    if reset_token:
        user = USERS.get(email)
        user["password"] = hash_password(new_password)
        return {"ok": True}
    return {"ok": False}
