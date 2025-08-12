import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FetchAlertDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        alert_id: str
    ) -> str:
        alerts = data.get("emergency_alerts", {})
        alert = alerts.get(alert_id)

        if not alert:
            return json.dumps({"error": f"Alert with ID {alert_id} not found."})

        return json.dumps(alert)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_alert_details",
                "description": "Fetch detailed information for a specific emergency alert by its alert ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_id": {
                            "type": "string",
                            "description": "The ID of the alert to retrieve"
                        }
                    },
                    "required": ["alert_id"]
                }
            }
        }
