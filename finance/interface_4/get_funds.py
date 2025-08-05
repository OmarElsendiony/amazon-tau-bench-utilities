import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        if not filters:
            filters = {}
        
        for fund in funds.values():
            # Apply filters
            if filters.get("fund_id") and fund.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("name") and filters["name"].lower() not in fund.get("name", "").lower():
                continue
            if filters.get("fund_type") and fund.get("fund_type") != filters["fund_type"]:
                continue
            if filters.get("base_currency") and fund.get("base_currency") != filters["base_currency"]:
                continue
            if filters.get("manager_id") and fund.get("manager_id") != filters["manager_id"]:
                continue
            if filters.get("status") and fund.get("status") != filters["status"]:
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get funds based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (fund_id, name, fund_type, base_currency, manager_id, status)"
                        }
                    },
                    "required": []
                }
            }
        }
