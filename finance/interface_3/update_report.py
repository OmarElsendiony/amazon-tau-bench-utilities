import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_id: str, status: str) -> str:
        reports = data.get("reports", {})
        
        # Validate report exists
        if str(report_id) not in reports:
            raise ValueError(f"Report {report_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        report = reports[str(report_id)]
        report["status"] = status
        report["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_report",
                "description": "Update a report's status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_id": {"type": "string", "description": "ID of the report"},
                        "status": {"type": "string", "description": "Report status (pending, completed, failed)"}
                    },
                    "required": ["report_id", "status"]
                }
            }
        }
