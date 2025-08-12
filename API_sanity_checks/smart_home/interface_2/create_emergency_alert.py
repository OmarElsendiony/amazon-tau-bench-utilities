import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateEmergencyAlert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               device_id: str,
               alert_type: str,
               severity_level: str,
               triggered_at: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        alerts = data.setdefault("emergency_alerts", {})
        alert_id = generate_id(alerts)

        alert_record = {
            "home_id": home_id,
            "device_id": device_id,
            "alert_type": alert_type,
            "severity_level": severity_level,
            "triggered_at": triggered_at,
            "acknowledged_at": None,
            "acknowledged_by_user": None,
            "resolved_at": None,
            "resolved_by_user": None,
            "created_at": triggered_at
        }

        alerts[alert_id] = alert_record

        return json.dumps({"alert_id": alert_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_emergency_alert",
                "description": "Create a new emergency alert for a device in a home.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "ID of the home where the alert was triggered"},
                        "device_id": {"type": "string", "description": "ID of the device causing the alert"},
                        "alert_type": {"type": "string", "description": "Type of alert, e.g. 'bulb_malfunction'"},
                        "severity_level": {"type": "string", "description": "Severity of alert (low, medium, high, critical)"},
                        "triggered_at": {"type": "string", "description": "ISO timestamp when the alert was triggered"}
                    },
                    "required": ["home_id", "device_id", "alert_type", "severity_level", "triggered_at"]
                }
            }
        }
