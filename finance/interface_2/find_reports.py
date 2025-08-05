import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FindReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            # Apply filters
            skip_report = False
            for key, value in filters.items():
                if key in report and report.get(key) != value:
                    skip_report = True
                    break
            
            if not skip_report:
                results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_reports",
                "description": "Find reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria for reports"}
                    },
                    "required": ["filters"]
                }
            }
        }
