import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FetchAlertsInfo(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        device_id: Optional[str] = None,
        severity_level: Optional[str] = None
    ) -> str:
        alerts = data.get("emergency_alerts", {})
        results = []

        for alert in alerts.values():
            if device_id is not None and str(alert.get("device_id")) != device_id:
                continue
            if severity_level is not None and alert.get("severity_level") != severity_level:
                continue
            results.append(alert)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_alerts_info",
                "description": "Fetch emergency alerts filtered by optional device ID and severity level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "Device ID to filter alerts"
                        },
                        "severity_level": {
                            "type": "string",
                            "description": "Severity of the alert (e.g., low, medium, high, critical)"
                        }
                    },
                    "required": []
                }
            }
        }
