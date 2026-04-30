"""
WebSocket endpoint for real-time updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.realtime.websocket import manager
from app.services.token_service import decode_token
import logging

logger = logging.getLogger("verity-ai.websocket")

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token")
):
    """
    WebSocket endpoint for real-time updates
    
    Connect with: ws://localhost:5000/api/ws?token=YOUR_JWT_TOKEN
    
    Message types received:
    - connection: Initial connection confirmation
    - verification_update: Status changes on loan verifications
    - document_processed: OCR and extraction complete
    - manager_action: Manager approved/rejected application
    """
    
    # Authenticate user from token
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
    except Exception as e:
        logger.error(f"WebSocket authentication failed: {e}")
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Connect user
    await manager.connect(websocket, user_id)
    
    try:
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            
            # Handle ping/pong for connection health
            if data == "ping":
                await manager.send_personal_message(
                    {"type": "pong", "timestamp": "now"},
                    websocket
                )
            else:
                # Echo back for debugging
                await manager.send_personal_message(
                    {"type": "echo", "message": data},
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected: user={user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "active_users": manager.get_active_users_count(),
        "total_connections": manager.get_total_connections_count()
    }
