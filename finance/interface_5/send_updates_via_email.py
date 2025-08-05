import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendUpdatesViaEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, subject: str,
               message_body: str, reference_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": "alert",
            "class": "reports",
            "reference_id": reference_id,
            "status": "sent",
            "sent_at": timestamp,
            "created_at": timestamp,
            "subject": subject,
            "message_body": message_body
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_updates_via_email",
                "description": "Send email updates/notifications",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Recipient email address"},
                        "subject": {"type": "string", "description": "Email subject"},
                        "message_body": {"type": "string", "description": "Email message body"},
                        "reference_id": {"type": "string", "description": "Optional reference ID for tracking"}
                    },
                    "required": ["email", "subject", "message_body"]
                }
            }
        }
