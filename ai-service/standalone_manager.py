"""
Standalone Manager Approval Router
No dependencies on old Beanie models
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.routers.manager_approval import router

__all__ = ["router"]
