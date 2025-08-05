import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveFundsWithFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: Optional[str] = None, manager_id: Optional[str] = None,
               size: Optional[float] = None, fund_type: Optional[str] = None, 
               base_currency: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            if manager_id and fund.get("manager_id") != manager_id:
                continue
            if size and fund.get("size") != size:
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
                "name": "retrieve_funds_with_filter",
                "description": "Retrieve funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name (partial match)"},
                        "manager_id": {"type": "string", "description": "Manager user ID"},
                        "size": {"type": "number", "description": "Fund size"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
