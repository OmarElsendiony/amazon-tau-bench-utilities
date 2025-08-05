import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_emergency_alert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               device_id: str,
               alert_type: str,
               severity_level: str,
               triggered_at: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        alerts = data.get("emergency_alerts", {})
        alert_id = generate_id(alerts)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_alert = {
            "alert_id": alert_id,
            "home_id": home_id,
            "device_id": device_id,
            "alert_type": alert_type,
            "severity_level": severity_level,
            "triggered_at": triggered_at,
            "acknowledged_at": None,
            "acknowledged_by_user": None,
            "resolved_at": None,
            "resolved_by_user": None,
            "created_at": timestamp
        }
        alerts[alert_id] = new_alert
        return json.dumps({"alert_id": alert_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_emergency_alert",
                "description": "Creates a new emergency alert for a device in a home",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "ID of the home"},
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "alert_type": {"type": "string", "description": "Type of alert"},
                        "severity_level": {"type": "string", "description": "Severity level (low, medium, high, critical)"},
                        "triggered_at": {"type": "string", "description": "Timestamp when alert was triggered"}
                    },
                    "required": ["home_id", "device_id", "alert_type", "severity_level", "triggered_at"]
                }
            }
        }
