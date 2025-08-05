import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], recipient_id: Optional[str] = None, status: Optional[str] = None) -> str:
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        results = []
        
        for notification in notifications.values():
            # Apply filters
            if recipient_id:
                # Find user by ID to get email
                user_email = None
                for user in users.values():
                    if str(user.get("user_id")) == str(recipient_id):
                        user_email = user.get("email")
                        break
                
                if not user_email or notification.get("email") != user_email:
                    continue
                    
            if status and notification.get("status") != status:
                continue
                
            results.append(notification)
        
        # Sort by created date (newest first)
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string", "description": "Filter by recipient user ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"}
                    },
                    "required": []
                }
            }
        }
