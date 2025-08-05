import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_investor_portfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                return json.dumps(portfolio)
        
        raise ValueError(f"Portfolio for investor {investor_id} not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get portfolio for a specific investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
