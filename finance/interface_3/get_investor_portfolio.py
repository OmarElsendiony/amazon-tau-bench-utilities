import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Find portfolio for the investor
        for portfolio in portfolios.values():
            if str(portfolio.get("investor_id")) == str(investor_id):
                return json.dumps(portfolio)
        
        # Return empty result if no portfolio found
        return json.dumps({})

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
