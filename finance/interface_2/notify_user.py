import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class NotifyUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, email: str, 
               type: str, reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": type,
            "class": "funds",  # Default class, could be made configurable
            "reference_id": str(reference_id),
            "status": "pending",
            "sent_at": None,
            "created_at": timestamp
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "notify_user",
                "description": "Create a notification for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to notify"},
                        "email": {"type": "string", "description": "Email address for notification"},
                        "type": {"type": "string", "description": "Notification type (alert, report, reminder, subscription_update)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["user_id", "email", "type", "reference_id"]
                }
            }
        }
