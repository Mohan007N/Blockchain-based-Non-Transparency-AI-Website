"""
Auth router — SQLite database version
POST /api/auth/register   — email/password signup
POST /api/auth/login      — email/password login
POST /api/auth/google    — Google One-Tap / OAuth
GET  /api/auth/me        — get own profile
PATCH /api/auth/me       — update own profile
"""

import os
import logging
from datetime import datetime
from typing import Optional
import uuid
import bcrypt

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from app.config.database import UserModel, async_session_maker
from app.services.token_service import build_token_response, get_current_user

logger = logging.getLogger("verity-ai.auth")
router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv(
    "GOOGLE_CLIENT_ID",
    "608687632539-2o6insdcvhdb2i1bvq6k6mcqart8rfq3.apps.googleusercontent.com",
)


# ── Schemas ──────────────────────────────────────────────────

class RegisterBody(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class GoogleLoginBody(BaseModel):
    id_token: str
    role: Optional[str] = "client"


class UpdateProfileBody(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None


# ── Helpers ─────────────────────────────────────────────────

def _verify_google_id_token(id_token: str) -> dict:
    """Verify a Google ID token using google-auth"""
    from google.oauth2 import id_token as google_id_token
    from google.auth.transport import requests as google_requests

    try:
        info = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
        return info
    except ValueError as e:
        logger.warning(f"Google token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google token.")


def _hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def _check_password(hashed: str, plain: str) -> bool:
    """Check password against hash"""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ── POST /api/auth/register ──────────────────────────────────

@router.post("/register", status_code=201)
async def register(body: RegisterBody):
    try:
        # Check if user exists
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == body.email)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(status_code=409, detail="Email already registered.")

            role = body.role if body.role in ("client", "manager") else "client"
            
            # Create new user
            user = UserModel(
                id=str(uuid.uuid4()),
                name=body.name,
                email=body.email,
                hashed_password=_hash_password(body.password),
                role=role,
                auth_provider="local",
                is_active=True,
                is_email_verified=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            logger.info(f"New user registered: {body.email} [{role}]")

            return {
                "success": True,
                "message": "Registration successful",
                **build_token_response(user),
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed.")


# ── POST /api/auth/login ─────────────────────────────────────

@router.post("/login")
async def login(body: LoginBody):
    try:
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserModel).where(
                    UserModel.email == body.email,
                    UserModel.auth_provider == "local"
                )
            )
            user = result.scalar_one_or_none()
            
            if not user or not _check_password(user.hashed_password or "", body.password):
                raise HTTPException(status_code=401, detail="Invalid email or password.")
            
            if not user.is_active:
                raise HTTPException(status_code=403, detail="Account deactivated.")

            # Update last login
            user.last_login = datetime.utcnow()
            await session.commit()

            return {
                "success": True,
                "message": "Login successful",
                **build_token_response(user),
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed.")


# ── POST /api/auth/google ─────────────────────────────────────

@router.post("/google")
async def google_login(body: GoogleLoginBody):
    try:
        google_info = _verify_google_id_token(body.id_token)
        
        email = google_info.get("email")
        name = google_info.get("name", google_info.get("email", "").split("@")[0])
        google_id = google_info.get("sub")
        photo_url = google_info.get("picture")
        
        if not email:
            raise HTTPException(status_code=400, detail="Invalid Google token payload.")

        async with async_session_maker() as session:
            # Check if user exists
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Create new user
                role = body.role if body.role in ("client", "manager") else "client"
                user = UserModel(
                    id=str(uuid.uuid4()),
                    name=name,
                    email=email,
                    role=role,
                    google_id=google_id,
                    auth_provider="google",
                    photo_url=photo_url,
                    is_active=True,
                    is_email_verified=True,
                    last_login=datetime.utcnow(),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(user)
            else:
                # Update existing user
                user.google_id = google_id
                user.photo_url = photo_url
                user.last_login = datetime.utcnow()
            
            await session.commit()
            await session.refresh(user)
            
            logger.info(f"Google login: {email} [{user.role}]")

            return {
                "success": True,
                "message": "Login successful",
                **build_token_response(user),
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google login error: {e}")
        raise HTTPException(status_code=500, detail="Google login failed.")


# ── GET /api/auth/me ─────────────────────────────────────────

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return {
        "success": True,
        "user": current_user.to_public(),
    }


# ── PATCH /api/auth/me ────────────────────────────────────────

@router.patch("/me")
async def update_profile(
    body: UpdateProfileBody,
    current_user = Depends(get_current_user),
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == current_user.id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")
            
            if body.name is not None:
                user.name = body.name
            if body.phone is not None:
                user.phone = body.phone
            if body.address is not None:
                user.address = body.address
            if body.pan_number is not None:
                user.pan_number = body.pan_number
            if body.aadhaar_number is not None:
                user.aadhaar_number = body.aadhaar_number
            
            user.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)
            
            return {
                "success": True,
                "message": "Profile updated",
                "user": user.to_public(),
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(status_code=500, detail="Profile update failed.")