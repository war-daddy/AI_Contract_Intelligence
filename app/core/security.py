# app/core/security.py

from datetime import datetime, timedelta
import jwt
from app.core.config import settings

def create_access_token(data: dict):
    """
    Generates JWT token with expiry.
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")