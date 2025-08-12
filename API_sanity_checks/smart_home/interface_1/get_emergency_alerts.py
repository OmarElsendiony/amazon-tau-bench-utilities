import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmergencyAlerts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        home_id: Optional[str] = None,
        device_id: Optional[str] = None,
        alert_type: Optional[str] = None,
        severity_level: Optional[str] = None,
        resolved_by_user: Optional[str] = None,
        acknowledged_by_user: Optional[str] = None
    ) -> str:
        alerts = data.get("emergency_alerts", {})
        results = []

        for alert in alerts.values():
            if home_id is not None and str(alert.get("home_id")) != home_id:
                continue
            if device_id is not None and str(alert.get("device_id")) != device_id:
                continue
            if alert_type is not None and alert.get("alert_type") != alert_type:
                continue
            if severity_level is not None and alert.get("severity_level") != severity_level:
                continue
            if resolved_by_user is not None and str(alert.get("resolved_by_user")) != resolved_by_user:
                continue
            if acknowledged_by_user is not None and str(alert.get("acknowledged_by_user")) != acknowledged_by_user:
                continue

            results.append(alert)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_emergency_alerts",
                "description": "Returns alerts filtered by home, device, type, severity, resolution, or acknowledgment user IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Home ID to filter alerts"},
                        "device_id": {"type": "string", "description": "Device ID to filter alerts"},
                        "alert_type": {"type": "string", "description": "Alert type (e.g., 'thermostat_offline')"},
                        "severity_level": {"type": "string", "description": "Severity of the alert (low/medium/high/critical)"},
                        "resolved_by_user": {"type": "string", "description": "User ID who resolved the alert"},
                        "acknowledged_by_user": {"type": "string", "description": "User ID who acknowledged the alert"}
                    },
                    "required": []
                }
            }
        }
