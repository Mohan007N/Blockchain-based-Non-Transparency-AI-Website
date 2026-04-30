"""
Standalone Auth Router - No dependencies on old models
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import uuid
import bcrypt
import httpx

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from jose import jwt, JWTError

from app.config.database import UserModel, async_session_maker

logger = logging.getLogger("verity-ai.auth")
router = APIRouter()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "change_me_in_production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_DAYS = 7

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "608687632539-2o6insdcvhdb2i1bvq6k6mcqart8rfq3.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "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")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/api/auth/google/callback")

bearer_scheme = HTTPBearer(auto_error=False)

# ── Schemas ──────────────────────────────────────────────────

class RegisterBody(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthBody(BaseModel):
    code: str
    redirect_uri: str


# ── Helpers ─────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def _check_password(hashed: str, plain: str) -> bool:
    """Check password against hash"""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRES_DAYS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def build_token_response(user) -> dict:
    token = create_token(str(user.id), user.role)
    return {
        "token": token,
        "token_type": "Bearer",
        "expires_in": JWT_EXPIRES_DAYS * 86400,
        "user": user.to_public(),
    }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="No token provided.")

    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    
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

    return user


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
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


# ── GET /api/auth/me ─────────────────────────────────────────

@router.get("/me")
async def get_me(current_user = Security(get_current_user)):
    return {
        "success": True,
        "user": current_user.to_public(),
    }


# ── GET /api/auth/google ─────────────────────────────────────

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth consent screen"""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return RedirectResponse(url=google_auth_url)


# ── GET /api/auth/google/callback ────────────────────────────

@router.get("/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange code for token")
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            # Get user info from Google
            user_info_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
            if user_info_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_info = user_info_response.json()
        
        # Create or update user in database
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == user_info["email"])
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Update existing user
                user.name = user_info.get("name", user.name)
                user.auth_provider = "google"
                user.google_id = user_info.get("id")
                user.is_email_verified = user_info.get("verified_email", False)
                user.last_login = datetime.utcnow()
                user.updated_at = datetime.utcnow()
            else:
                # Create new user
                user = UserModel(
                    id=str(uuid.uuid4()),
                    name=user_info.get("name", "Google User"),
                    email=user_info["email"],
                    role="client",
                    auth_provider="google",
                    google_id=user_info.get("id"),
                    is_active=True,
                    is_email_verified=user_info.get("verified_email", False),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    last_login=datetime.utcnow(),
                )
                session.add(user)
            
            await session.commit()
            await session.refresh(user)
            
            # Create JWT token
            token = create_token(str(user.id), user.role)
            
            # Redirect to frontend with token
            frontend_url = f"http://localhost:8080/auth?token={token}&user={user.email}"
            return RedirectResponse(url=frontend_url)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")


# ── POST /api/auth/google/token ──────────────────────────────

@router.post("/google/token")
async def google_token_auth(body: GoogleAuthBody):
    """Exchange Google authorization code for JWT token (for frontend flow)"""
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": body.code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": body.redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange code for token")
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            # Get user info from Google
            user_info_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
            if user_info_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_info = user_info_response.json()
        
        # Create or update user in database
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == user_info["email"])
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Update existing user
                user.name = user_info.get("name", user.name)
                user.auth_provider = "google"
                user.google_id = user_info.get("id")
                user.is_email_verified = user_info.get("verified_email", False)
                user.last_login = datetime.utcnow()
                user.updated_at = datetime.utcnow()
            else:
                # Create new user
                user = UserModel(
                    id=str(uuid.uuid4()),
                    name=user_info.get("name", "Google User"),
                    email=user_info["email"],
                    role="client",
                    auth_provider="google",
                    google_id=user_info.get("id"),
                    is_active=True,
                    is_email_verified=user_info.get("verified_email", False),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    last_login=datetime.utcnow(),
                )
                session.add(user)
            
            await session.commit()
            await session.refresh(user)
            
            logger.info(f"Google OAuth login: {user.email}")
            
            return {
                "success": True,
                "message": "Google authentication successful",
                **build_token_response(user),
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google token auth error: {e}")
        raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")
