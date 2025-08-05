import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class acknowledge_or_resolve_alert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_id: str,
               acknowledged_at: Optional[str] = None,
               acknowledged_by_user: Optional[str] = None,
               resolved_at: Optional[str] = None,
               resolved_by_user: Optional[str] = None) -> str:

        alerts = data.get("emergency_alerts", {})

        # Fetch and validate alert
        alert = alerts.get(alert_id)
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        # Update fields if provided
        if acknowledged_at is not None:
            alert["acknowledged_at"] = acknowledged_at
        if acknowledged_by_user is not None:
            alert["acknowledged_by_user"] = acknowledged_by_user
        if resolved_at is not None:
            alert["resolved_at"] = resolved_at
        if resolved_by_user is not None:
            alert["resolved_by_user"] = resolved_by_user

        # Stamp update time
        alert["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(alert)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "acknowledge_or_resolve_alert",
                "description": "Acknowledges or resolves an emergency alert by updating its timestamps and users",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_id": {"type": "string", "description": "ID of the alert"},
                        "acknowledged_at": {"type": "string", "description": "Timestamp of acknowledgment"},
                        "acknowledged_by_user": {"type": "string", "description": "User ID who acknowledged"},
                        "resolved_at": {"type": "string", "description": "Timestamp of resolution"},
                        "resolved_by_user": {"type": "string", "description": "User ID who resolved"}
                    },
                    "required": ["alert_id"]
                }
            }
        }
