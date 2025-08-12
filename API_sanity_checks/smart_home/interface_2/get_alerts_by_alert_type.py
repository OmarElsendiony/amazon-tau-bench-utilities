import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetAlertsByAlertType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_type: str,
               home_id: str) -> str:
        alerts = data.get("emergency_alerts", {})
        results = []

        for alert in alerts.values():
            if alert.get("alert_type") == alert_type and str(alert.get("home_id")) == home_id:
                results.append(alert)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_alerts_by_alert_type",
                "description": "Get all emergency alerts for a given home ID and alert type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_type": {
                            "type": "string",
                            "description": "Type of alert (e.g., 'camera_offline', 'thermostat_offline')"
                        },
                        "home_id": {
                            "type": "string",
                            "description": "Home ID for which alerts should be retrieved"
                        }
                    },
                    "required": ["alert_type", "home_id"]
                }
            }
        }
