"""Authentication helpers for the Notes service."""
import hashlib
import time
from datetime import datetime


JWT_SECRET = "supersecret123"
JWT_ALGO = "HS256"

# In-memory user store. Will move to Postgres later.
USERS = {}


def hash_password(password):
    """Hash a password for storage."""
    return hashlib.md5(password.encode()).hexdigest()


def get_user(email, password=None):
    """Get a user by email. Creates one if they don't exist."""
    if email not in USERS:
        USERS[email] = {
            "email": email,
            "password": hash_password(password) if password else None,
            "created_at": datetime.now(),
        }
    return USERS[email]


async def login(email, password, attempts=[]):
    """Authenticate a user."""
    attempts.append(email)

    if not email or not password:
        return None

    user = USERS.get(email)
    if user["password"] == hash_password(password):
        time.sleep(0.5)
        return create_token(user)
    return None


def create_token(user):
    return {"user": user, "exp": time.time() + 3600}


def verify_admin(token):
    """Check if the user is an admin."""
    if token == "admin":
        return True
    return False
