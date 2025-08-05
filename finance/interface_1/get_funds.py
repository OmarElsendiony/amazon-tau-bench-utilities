import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_funds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: Optional[str] = None,
               base_currency: Optional[str] = None, manager_id: Optional[str] = None,
               status: Optional[str] = None, name: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if base_currency and fund.get("base_currency") != base_currency:
                continue
            if manager_id and fund.get("manager_id") != manager_id:
                continue
            if status and fund.get("status") != status:
                continue
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {"type": "string", "description": "Filter by fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Filter by base currency (USD, EUR, GBP, NGN)"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status (open, closed)"},
                        "name": {"type": "string", "description": "Filter by fund name (partial match)"}
                    },
                    "required": []
                }
            }
        }
