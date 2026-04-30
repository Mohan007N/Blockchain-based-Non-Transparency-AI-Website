"""
Verity AI - Backend with Authentication
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.config.database import init_db
from standalone_auth import router as auth_router
from standalone_loan import router as loan_router
from standalone_manager import router as manager_router

# Startup/Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Verity AI Backend starting...")
    await init_db()
    print("✅ Database initialized")
    yield
    print("👋 Verity AI Backend shutting down")

# FastAPI app
app = FastAPI(
    title="Verity AI",
    description="AI-powered Bank Loan Document Verification",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Verity AI Backend",
        "version": "2.0.0",
        "database": "SQLite",
        "features": {
            "auth": True,
            "blockchain": False,
            "websocket": True,
            "real_time": True
        }
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Verity AI API",
        "docs": "/api/docs",
        "health": "/api/health",
        "endpoints": {
            "auth": "/api/auth/*",
            "register": "/api/auth/register",
            "login": "/api/auth/login"
        }
    }

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(loan_router, prefix="/api/loans", tags=["Loan Verification"])
app.include_router(manager_router, prefix="/api/manager", tags=["Manager Approval"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_with_auth:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info",
    )
