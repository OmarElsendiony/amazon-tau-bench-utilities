import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class EmailUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, class_: str, reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if class_ not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")
        
        user = users[str(user_id)]
        user_email = user.get("email")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_notification = {
            "notification_id": notification_id,
            "email": user_email,
            "type": "alert",
            "class": class_,
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
                "name": "email_user",
                "description": "Send an email notification to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to email"},
                        "class": {"type": "string", "description": "Class of notification (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["user_id", "class", "reference_id"]
                }
            }
        }
