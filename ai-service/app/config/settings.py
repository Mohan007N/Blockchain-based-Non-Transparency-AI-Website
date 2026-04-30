"""
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Server
    host: str = "0.0.0.0"
    port: int = 5000
    environment: str = "development"
    debug: bool = True
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./verity_ai.db"
    sql_echo: bool = False
    
    # JWT
    jwt_secret: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expires_in: str = "7d"
    
    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    # Google Cloud Vision
    google_application_credentials: Optional[str] = None
    gcp_project_id: Optional[str] = None
    
    # File Upload
    upload_dir: str = "./uploads"
    max_file_size: int = 15728640  # 15MB
    allowed_extensions: str = "pdf,jpg,jpeg,png"
    
    # Blockchain
    blockchain_network: str = "ganache"
    blockchain_rpc_url: str = "http://127.0.0.1:8545"
    blockchain_private_key: Optional[str] = None
    contract_address: Optional[str] = None
    enable_blockchain: bool = True
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    enable_redis: bool = False
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    enable_sentry: bool = False
    prometheus_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # WebSocket
    websocket_enabled: bool = True
    websocket_ping_interval: int = 30
    websocket_ping_timeout: int = 10
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins into list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions into list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
