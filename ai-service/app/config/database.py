"""
SQLite database configuration using SQLAlchemy async
Replaces MongoDB with SQLite for better local development
"""

import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from datetime import datetime

logger = logging.getLogger("verity-ai.db")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///verity_ai.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    future=True,
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

_db_available = False


class Base(DeclarativeBase):
    pass


# ── User Model ─────────────────────────────────────────────
class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, default="client")  # client, manager, admin
    google_id = Column(String, nullable=True)
    auth_provider = Column(String, default="local")
    photo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    pan_number = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_public(self) -> dict:
        """Convert user model to public dict"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "auth_provider": self.auth_provider,
            "photo_url": self.photo_url,
            "is_active": self.is_active,
            "is_email_verified": self.is_email_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── Loan Verification Model ───────────────────────────────
class LoanVerificationModel(Base):
    __tablename__ = "loan_verifications"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    application_id = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, processing, ai_reviewed, approved, rejected
    result = Column(String, nullable=True)  # Approved, Rejected, Under Review
    reason = Column(String, nullable=True)
    
    # Extracted data
    document_type = Column(String, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    
    # AI Decision
    ai_decision = Column(JSON, nullable=True)
    
    # File tracking
    file_name = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ── Eligibility Submission Model ─────────────────────────
class EligibilitySubmissionModel(Base):
    __tablename__ = "eligibility_submissions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    loan_type = Column(String, nullable=True)
    loan_amount = Column(Float, nullable=True)
    income_proof = Column(String, nullable=True)  # ZKP proof
    credit_score_proof = Column(String, nullable=True)  # ZKP proof
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")


async def init_db():
    """Initialize database and create tables"""
    global _db_available
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _db_available = True
        logger.info("✅ SQLite database initialized")
    except Exception as e:
        _db_available = False
        logger.warning(f"⚠️  Database initialization error: {e}")


def get_client():
    return engine


def is_db_available() -> bool:
    return _db_available


async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        yield session


async def get_db():
    """Dependency for FastAPI routes"""
    async with async_session_maker() as session:
        yield session


def get_in_memory_store() -> dict:
    return _in_memory_store
