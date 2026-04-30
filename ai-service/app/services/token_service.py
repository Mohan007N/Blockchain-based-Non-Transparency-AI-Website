"""
JWT token service — SQLite database version
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from app.config.database import UserModel, async_session_maker

JWT_SECRET = os.getenv("JWT_SECRET", "change_me_in_production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_DAYS = int(os.getenv("JWT_EXPIRES_DAYS", 7))

bearer_scheme = HTTPBearer(auto_error=False)


def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRES_DAYS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


def build_token_response(user) -> dict:
    token = create_token(str(user.id), user.role)
    return {
        "token": token,
        "token_type": "Bearer",
        "expires_in": JWT_EXPIRES_DAYS * 86400,
        "user": user.to_public(),
    }


# ── User wrapper class for token service ─────────────────────
class TokenUser:
    """Wrapper class to provide consistent interface for token service"""
    
    def __init__(self, user_model: UserModel):
        self.id = user_model.id
        self.email = user_model.email
        self.name = user_model.name
        self.role = user_model.role
        self.photo_url = user_model.photo_url
        self.is_email_verified = user_model.is_email_verified
        self.last_login = user_model.last_login
        self.created_at = user_model.created_at
        self.is_active = user_model.is_active
    
    def to_public(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "auth_provider": "local",
            "photo_url": self.photo_url,
            "is_active": self.is_active,
            "is_email_verified": self.is_email_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── FastAPI dependency ──────────────────────────────────────

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="No token provided.")

    payload = decode_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload.")

    # Get user from database
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated.")

    return TokenUser(user)


async def require_manager(user=Depends(get_current_user)):
    if user.role not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Manager role required.")
    return user