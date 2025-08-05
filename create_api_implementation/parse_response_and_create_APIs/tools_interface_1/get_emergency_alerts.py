import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_emergency_alerts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               device_id: Optional[str] = None,
               alert_type: Optional[str] = None,
               severity_level: Optional[str] = None,
               acknowledged_by_user: Optional[str] = None,
               resolved_by_user: Optional[str] = None) -> str:

        results = []
        for alert in data.get("emergency_alerts", {}).values():
            if home_id and alert.get("home_id") != home_id:
                continue
            if device_id and alert.get("device_id") != device_id:
                continue
            if alert_type and alert.get("alert_type") != alert_type:
                continue
            if severity_level and alert.get("severity_level") != severity_level:
                continue
            if acknowledged_by_user and str(alert.get("acknowledged_by_user")) != acknowledged_by_user:
                continue
            if resolved_by_user and str(alert.get("resolved_by_user")) != resolved_by_user:
                continue
            results.append(alert)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_emergency_alerts",
                "description": "Returns alerts filtered by home, device, alert type, severity, or user IDs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "device_id": {"type": "string", "description": "Filter by device ID"},
                        "alert_type": {"type": "string", "description": "Filter by alert type"},
                        "severity_level": {"type": "string", "description": "Filter by severity level"},
                        "acknowledged_by_user": {"type": "string", "description": "Filter by acknowledging user ID"},
                        "resolved_by_user": {"type": "string", "description": "Filter by resolving user ID"}
                    },
                    "required": []
                }
            }
        }
