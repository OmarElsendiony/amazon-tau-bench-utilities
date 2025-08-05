import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListFundsWithFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               name: Optional[str] = None, fund_type: Optional[str] = None,
               base_currency: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_id and fund.get("fund_id") != fund_id:
                continue
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if base_currency and fund.get("base_currency") != base_currency:
                continue
            if status and fund.get("status") != status:
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_funds_with_filter",
                "description": "List funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "name": {"type": "string", "description": "Filter by fund name (partial match)"},
                        "fund_type": {"type": "string", "description": "Filter by fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Filter by base currency (USD, EUR, GBP, NGN)"},
                        "status": {"type": "string", "description": "Filter by status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
