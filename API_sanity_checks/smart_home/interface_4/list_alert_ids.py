import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ListAlertIds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_type: Optional[str] = None,
               acknowledged_by_user: Optional[str] = None,
               resolved_by_user: Optional[str] = None) -> str:
        """
        Returns a list of alert IDs filtered by optional parameters.
        """
        emergency_alerts = data.get("emergency_alerts", {})
        result = []

        for alert_id, alert in emergency_alerts.items():
            if alert_type and alert.get("alert_type") != alert_type:
                continue
            if acknowledged_by_user and str(alert.get("acknowledged_by_user")) != acknowledged_by_user:
                continue
            if resolved_by_user and str(alert.get("resolved_by_user")) != resolved_by_user:
                continue

            result.append({"alert_id": str(alert_id)})

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_alert_ids",
                "description": "List alert IDs based on optional filters like alert type, acknowledged by user, and resolved by user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_type": {
                            "type": "string",
                            "description": "Filter by alert type (e.g., bulb_malfunction, refrigerator_malfunction)"
                        },
                        "acknowledged_by_user": {
                            "type": "string",
                            "description": "Filter by user ID who acknowledged the alert"
                        },
                        "resolved_by_user": {
                            "type": "string",
                            "description": "Filter by user ID who resolved the alert"
                        }
                    },
                    "required": []
                }
            }
        }