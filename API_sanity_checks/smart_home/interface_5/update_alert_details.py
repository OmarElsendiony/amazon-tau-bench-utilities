import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateAlertDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_id: str,
               device_id: str = None,
               alert_type: str = None,
               acknowledged_at: str = None,
               acknowledged_by_user: str = None,
               resolved_at: str = None,
               resolved_by_user: str = None,
               severity_level: str = None) -> str:
        
        alerts = data.get("emergency_alerts", {})
        alert = alerts.get(alert_id)

        if not alert:
            raise ValueError(f"Alert with ID {alert_id} not found.")

        default_time = "2025-10-01T00:00:00"

        if device_id is not None:
            alert["device_id"] = device_id
        if alert_type is not None:
            alert["alert_type"] = alert_type
        if acknowledged_by_user is not None:
            alert["acknowledged_by_user"] = acknowledged_by_user
            alert["acknowledged_at"] = acknowledged_at or default_time
        if resolved_by_user is not None:
            alert["resolved_by_user"] = resolved_by_user
            alert["resolved_at"] = resolved_at or default_time
        if severity_level is not None:
            alert["severity_level"] = severity_level

        return json.dumps(alert)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_alert_details",
                "description": "Update an alert with optional details like device ID, type, acknowledgment, resolution, and severity. Defaults timestamps if missing.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_id": {
                            "type": "string",
                            "description": "The ID of the alert to update"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Device ID associated with the alert"
                        },
                        "alert_type": {
                            "type": "string",
                            "description": "Type of the alert (e.g., 'camera_offline')"
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
                        },
                        "severity_level": {
                            "type": "string",
                            "description": "Severity level (low, medium, high, critical)"
                        }
                    },
                    "required": ["alert_id"]
                }
            }
        }
