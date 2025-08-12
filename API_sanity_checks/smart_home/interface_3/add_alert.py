import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddAlert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               alert_type: str,
               severity_level: str,
               triggered_at: str) -> str:

        alerts = data.setdefault("emergency_alerts", {})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        alert_id = generate_id(alerts)
        timestamp = "2025-10-01T00:00:00"

        new_alert = {
            "alert_id": alert_id,
            "device_id": device_id,
            "alert_type": alert_type,
            "severity_level": severity_level,
            "triggered_at": triggered_at,
            "acknowledged_at": None,
            "acknowledged_by_user": None,
            "resolved_at": None,
            "resolved_by_user": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        alerts[alert_id] = new_alert
        return json.dumps({"alert_id": alert_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_alert",
                "description": "Add a new emergency alert with device, type, severity, and trigger timestamp.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "The ID of the device that triggered the alert"
                        },
                        "alert_type": {
                            "type": "string",
                            "description": "Type of alert (e.g., fire, intrusion, power outage)"
                        },
                        "severity_level": {
                            "type": "string",
                            "description": "Severity level of the alert (e.g., low, medium, high)"
                        },
                        "triggered_at": {
                            "type": "string",
                            "description": "Timestamp when the alert was triggered"
                        }
                    },
                    "required": ["device_id", "alert_type", "severity_level", "triggered_at"]
                }
            }
        }
