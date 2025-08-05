import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        if not filters:
            filters = {}
        
        for report in reports.values():
            # Apply filters
            if filters.get("report_id") and report.get("report_id") != filters["report_id"]:
                continue
            if filters.get("fund_id") and report.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and report.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("report_type") and report.get("report_type") != filters["report_type"]:
                continue
            if filters.get("generated_by") and report.get("generated_by") != filters["generated_by"]:
                continue
            if filters.get("status") and report.get("status") != filters["status"]:
                continue
            
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reports",
                "description": "Retrieve reports based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (report_id, fund_id, investor_id, report_type, generated_by, status)"
                        }
                    },
                    "required": []
                }
            }
        }
