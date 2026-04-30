"""
User model wrapper
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User model for authentication and authorization"""
    id: str
    email: EmailStr
    name: str
    role: str = "client"  # client, manager, admin
    google_id: Optional[str] = None
    auth_provider: str = "local"
    photo_url: Optional[str] = None
    is_active: bool = True
    is_email_verified: bool = False
    last_login: Optional[datetime] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
