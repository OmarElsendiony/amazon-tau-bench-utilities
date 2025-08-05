import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, report_type: Optional[str] = None,
               report_date: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            if fund_id and report.get("fund_id") != fund_id:
                continue
            if investor_id and report.get("investor_id") != investor_id:
                continue
            if report_type and report.get("report_type") != report_type:
                continue
            if report_date and report.get("report_date") != report_date:
                continue
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reports",
                "description": "Get reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "report_date": {"type": "string", "description": "Filter by report date"}
                    },
                    "required": []
                }
            }
        }
