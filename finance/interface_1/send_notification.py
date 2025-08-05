import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str, reference_id: str,
               recipient_id: Optional[str] = None, email: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate at least one recipient method is provided
        if not recipient_id and not email:
            raise ValueError("Either recipient_id or email must be provided")
        
        # If recipient_id is provided, validate user exists and get email
        recipient_email = email
        if recipient_id:
            if str(recipient_id) not in users:
                raise ValueError(f"User {recipient_id} not found")
            recipient_email = users[str(recipient_id)].get("email")
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": notification_id,
            "email": recipient_email,
            "type": type,
            "class": "subscriptions",  # Default class based on common use case
            "reference_id": reference_id,
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
                "name": "send_notification",
                "description": "Send a notification to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string", "description": "ID of the recipient user (optional if email is provided)"},
                        "email": {"type": "string", "description": "Email address of the recipient (optional if recipient_id is provided)"},
                        "type": {"type": "string", "description": "Type of notification (alert, report, reminder, subscription_update)"},
                        "reference_id": {"type": "string", "description": "ID of the related record"}
                    },
                    "required": ["type", "reference_id"]
                }
            }
        }
