import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, report_date: str, 
               report_type: str, generated_by: str, export_period_end: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": report_date,
            "report_type": report_type,
            "generated_by": generated_by,
            "status": "pending",
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[str(report_id)] = new_report
        return json.dumps(new_report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a new report for a fund and investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_date": {"type": "string", "description": "Date of the report (YYYY-MM-DD)"},
                        "report_type": {"type": "string", "description": "Type of report (performance, holding, financial)"},
                        "generated_by": {"type": "string", "description": "ID of the user generating the report"},
                        "export_period_end": {"type": "string", "description": "End date of the export period (YYYY-MM-DD)"}
                    },
                    "required": ["fund_id", "investor_id", "report_date", "report_type", "generated_by", "export_period_end"]
                }
            }
        }
