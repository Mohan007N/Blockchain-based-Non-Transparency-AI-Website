"""
Manager Approval Router
Allows managers to review and approve/reject loan applications
"""

import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select, or_

from app.config.database import UserModel, LoanVerificationModel, async_session_maker
from standalone_auth import get_current_user

logger = logging.getLogger("verity-ai.manager")
router = APIRouter()


def require_manager(current_user: UserModel = Depends(get_current_user)):
    """Dependency to ensure user is a manager"""
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Manager or admin role required"
        )
    return current_user


class ApprovalAction(BaseModel):
    application_id: str
    action: str  # "approve" or "reject"
    comment: Optional[str] = None


@router.get("/pending")
async def get_pending_applications(
    manager: UserModel = Depends(require_manager)
):
    """Get all applications pending manager approval"""
    try:
        async with async_session_maker() as session:
            result = await session.execute(
                select(LoanVerificationModel)
                .where(LoanVerificationModel.status == "pending_manager_approval")
                .order_by(LoanVerificationModel.created_at.desc())
            )
            applications = result.scalars().all()
            
            # Get user details for each application
            app_list = []
            for app in applications:
                user_result = await session.execute(
                    select(UserModel).where(UserModel.id == app.user_id)
                )
                user = user_result.scalar_one_or_none()
                
                app_list.append({
                    "id": app.id,
                    "application_id": app.application_id,
                    "user": {
                        "id": user.id if user else None,
                        "name": user.name if user else "Unknown",
                        "email": user.email if user else "Unknown"
                    },
                    "loan_type": app.extracted_data.get("loan_type") if app.extracted_data else None,
                    "loan_amount": app.extracted_data.get("loan_amount") if app.extracted_data else None,
                    "status": app.status,
                    "verification_result": app.ai_decision,
                    "created_at": app.created_at.isoformat() if app.created_at else None,
                    "blockchain_hash": app.ai_decision.get("blockchain_hash") if app.ai_decision else None
                })
            
            return {
                "success": True,
                "count": len(app_list),
                "applications": app_list
            }
    except Exception as e:
        logger.error(f"Error fetching pending applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_applications(
    status: Optional[str] = None,
    manager: UserModel = Depends(require_manager)
):
    """Get all applications with optional status filter"""
    try:
        async with async_session_maker() as session:
            query = select(LoanVerificationModel)
            
            if status:
                query = query.where(LoanVerificationModel.status == status)
            
            query = query.order_by(LoanVerificationModel.created_at.desc())
            result = await session.execute(query)
            applications = result.scalars().all()
            
            # Get user details
            app_list = []
            for app in applications:
                user_result = await session.execute(
                    select(UserModel).where(UserModel.id == app.user_id)
                )
                user = user_result.scalar_one_or_none()
                
                app_list.append({
                    "id": app.id,
                    "application_id": app.application_id,
                    "user": {
                        "id": user.id if user else None,
                        "name": user.name if user else "Unknown",
                        "email": user.email if user else "Unknown"
                    },
                    "loan_type": app.extracted_data.get("loan_type") if app.extracted_data else None,
                    "loan_amount": app.extracted_data.get("loan_amount") if app.extracted_data else None,
                    "status": app.status,
                    "result": app.result,
                    "reason": app.reason,
                    "created_at": app.created_at.isoformat() if app.created_at else None
                })
            
            return {
                "success": True,
                "count": len(app_list),
                "applications": app_list
            }
    except Exception as e:
        logger.error(f"Error fetching applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/approve")
async def approve_application(
    action: ApprovalAction,
    manager: UserModel = Depends(require_manager)
):
    """Approve or reject a loan application"""
    try:
        if action.action not in ["approve", "reject"]:
            raise HTTPException(
                status_code=400,
                detail="Action must be 'approve' or 'reject'"
            )
        
        async with async_session_maker() as session:
            result = await session.execute(
                select(LoanVerificationModel)
                .where(LoanVerificationModel.application_id == action.application_id)
            )
            application = result.scalar_one_or_none()
            
            if not application:
                raise HTTPException(status_code=404, detail="Application not found")
            
            if application.status != "pending_manager_approval":
                raise HTTPException(
                    status_code=400,
                    detail=f"Application is not pending approval (current status: {application.status})"
                )
            
            # Update application
            if action.action == "approve":
                application.status = "approved"
                application.result = "Approved"
                application.reason = action.comment or "Approved by manager"
            else:
                application.status = "rejected"
                application.result = "Rejected"
                application.reason = action.comment or "Rejected by manager"
            
            application.updated_at = datetime.utcnow()
            
            # Store manager action in ai_decision
            if not application.ai_decision:
                application.ai_decision = {}
            
            application.ai_decision["manager_action"] = {
                "manager_id": manager.id,
                "manager_name": manager.name,
                "action": action.action,
                "comment": action.comment,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await session.commit()
            
            logger.info(
                f"Application {action.application_id} {action.action}d by manager {manager.name}"
            )
            
            return {
                "success": True,
                "message": f"Application {action.action}d successfully",
                "application_id": action.application_id,
                "status": application.status
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing approval: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_manager_stats(manager: UserModel = Depends(require_manager)):
    """Get statistics for manager dashboard"""
    try:
        async with async_session_maker() as session:
            # Count by status
            pending_result = await session.execute(
                select(LoanVerificationModel)
                .where(LoanVerificationModel.status == "pending_manager_approval")
            )
            pending_count = len(pending_result.scalars().all())
            
            approved_result = await session.execute(
                select(LoanVerificationModel)
                .where(LoanVerificationModel.status == "approved")
            )
            approved_count = len(approved_result.scalars().all())
            
            rejected_result = await session.execute(
                select(LoanVerificationModel)
                .where(LoanVerificationModel.status == "rejected")
            )
            rejected_count = len(rejected_result.scalars().all())
            
            return {
                "success": True,
                "stats": {
                    "pending": pending_count,
                    "approved": approved_count,
                    "rejected": rejected_count,
                    "total": pending_count + approved_count + rejected_count
                }
            }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
