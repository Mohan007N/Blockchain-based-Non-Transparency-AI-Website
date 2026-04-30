"""
WebSocket manager for real-time updates
Sends live notifications to clients about verification status changes
"""

import logging
import json
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger("verity-ai.websocket")


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # user_id -> Set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # websocket -> user_id mapping for cleanup
        self.connection_users: Dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.connection_users[websocket] = user_id
        
        logger.info(f"WebSocket connected: user={user_id}, total={len(self.active_connections[user_id])}")
        
        # Send welcome message
        await self.send_personal_message(
            {
                "type": "connection",
                "status": "connected",
                "message": "Real-time updates enabled",
                "timestamp": datetime.utcnow().isoformat()
            },
            websocket
        )
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        user_id = self.connection_users.get(websocket)
        
        if user_id and user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if websocket in self.connection_users:
            del self.connection_users[websocket]
        
        logger.info(f"WebSocket disconnected: user={user_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific WebSocket connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.disconnect(websocket)
    
    async def send_to_user(self, message: dict, user_id: str):
        """Send message to all connections of a specific user"""
        if user_id not in self.active_connections:
            logger.debug(f"No active connections for user: {user_id}")
            return
        
        # Create a copy to avoid modification during iteration
        connections = list(self.active_connections[user_id])
        
        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to user {user_id}: {e}")
                self.disconnect(connection)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for user_id, connections in list(self.active_connections.items()):
            for connection in list(connections):
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Broadcast failed for user {user_id}: {e}")
                    self.disconnect(connection)
    
    async def notify_verification_update(
        self,
        user_id: str,
        verification_id: str,
        status: str,
        data: Optional[dict] = None
    ):
        """Send verification status update to user"""
        message = {
            "type": "verification_update",
            "verification_id": verification_id,
            "status": status,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_user(message, user_id)
        logger.info(f"Sent verification update: user={user_id}, status={status}")
    
    async def notify_document_processed(
        self,
        user_id: str,
        verification_id: str,
        extracted_data: dict
    ):
        """Notify user that document processing is complete"""
        message = {
            "type": "document_processed",
            "verification_id": verification_id,
            "extracted_data": extracted_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_user(message, user_id)
    
    async def notify_manager_action(
        self,
        user_id: str,
        verification_id: str,
        action: str,
        manager_name: str,
        comment: str = ""
    ):
        """Notify user of manager action on their application"""
        message = {
            "type": "manager_action",
            "verification_id": verification_id,
            "action": action,
            "manager_name": manager_name,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_user(message, user_id)
    
    def get_active_users_count(self) -> int:
        """Get count of users with active connections"""
        return len(self.active_connections)
    
    def get_total_connections_count(self) -> int:
        """Get total number of active WebSocket connections"""
        return sum(len(connections) for connections in self.active_connections.values())


# Global connection manager instance
manager = ConnectionManager()
