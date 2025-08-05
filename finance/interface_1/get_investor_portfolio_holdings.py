import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_investor_portfolio_holdings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        results = []
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == portfolio_id:
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio_holdings",
                "description": "Get holdings for a specific portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["portfolio_id"]
                }
            }
        }
