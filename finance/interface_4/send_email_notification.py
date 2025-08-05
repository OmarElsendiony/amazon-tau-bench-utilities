import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SendEmailNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, class_name: str,
               reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        # Validate class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if class_name not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": "alert",
            "class": class_name,
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
                "name": "send_email_notification",
                "description": "Send an email notification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address to send notification to"},
                        "class_name": {"type": "string", "description": "Notification class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["email", "class_name", "reference_id"]
                }
            }
        }
