import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateAlert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_id: str,
               device_id: str = None,
               acknowledged_at: str = None,
               acknowledged_by_user: str = None,
               resolved_at: str = None,
               resolved_by_user: str = None) -> str:
        
        alerts = data.get("emergency_alerts", {})
        alert = alerts.get(alert_id)

        if not alert:
            raise ValueError(f"Alert with ID {alert_id} not found.")

        default_time = "2025-10-01T00:00:00"

        # Optional device update
        if device_id is not None:
            alert["device_id"] = device_id

        # Acknowledgment handling
        if acknowledged_by_user is not None:
            alert["acknowledged_by_user"] = acknowledged_by_user
            alert["acknowledged_at"] = acknowledged_at or default_time

        # Resolution handling
        if resolved_by_user is not None:
            alert["resolved_by_user"] = resolved_by_user
            alert["resolved_at"] = resolved_at or default_time

        return json.dumps(alert)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_alert",
                "description": "Update an emergency alert's device_id, acknowledgment, or resolution. Timestamps default to 2025-10-01T00:00:00 if not provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_id": {
                            "type": "string",
                            "description": "The ID of the emergency alert to update"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Device ID related to the alert"
                        },
                        "acknowledged_at": {
                            "type": "string",
                            "description": "Timestamp when the alert was acknowledged"
                        },
                        "acknowledged_by_user": {
                            "type": "string",
                            "description": "User ID who acknowledged the alert"
                        },
                        "resolved_at": {
                            "type": "string",
                            "description": "Timestamp when the alert was resolved"
                        },
                        "resolved_by_user": {
                            "type": "string",
                            "description": "User ID who resolved the alert"
                        }
                    },
                    "required": ["alert_id"]
                }
            }
        }
