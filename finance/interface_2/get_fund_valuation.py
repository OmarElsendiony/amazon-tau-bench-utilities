import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetFundValuation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, date: str) -> str:
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        # Find NAV record for the fund on the specified date
        nav_value = None
        nav_details = None
        
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id and nav.get("nav_date") == date:
                nav_value = nav.get("nav_value")
                nav_details = nav
                break
        
        if nav_value is None:
            raise ValueError(f"No NAV record found for fund {fund_id} on date {date}")
        
        # Get fund details
        fund_details = None
        for fund in funds.values():
            if fund.get("fund_id") == fund_id:
                fund_details = fund
                break
        
        result = {
            "valuation": float(nav_value),
            "fund_id": fund_id,
            "nav_details": nav_details
        }
        
        if fund_details:
            result["fund_details"] = fund_details
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_valuation",
                "description": "Get fund valuation for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "date"]
                }
            }
        }
