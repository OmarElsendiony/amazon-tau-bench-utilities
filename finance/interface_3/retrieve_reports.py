import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, investor_id: Optional[str] = None, report_type: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            # Apply filters
            if fund_id and str(report.get("fund_id")) != str(fund_id):
                continue
            if investor_id and str(report.get("investor_id")) != str(investor_id):
                continue
            if report_type and report.get("report_type") != report_type:
                continue
                
            results.append(report)
        
        # Sort by report date (newest first)
        results.sort(key=lambda x: x.get("report_date", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reports",
                "description": "Retrieve reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"}
                    },
                    "required": []
                }
            }
        }
