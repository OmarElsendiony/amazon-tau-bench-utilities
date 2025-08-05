import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolios = data.get("portfolios", {})
        holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        results = []
        for holding in holdings.values():
            if str(holding.get("portfolio_id")) == str(portfolio_id):
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_holdings",
                "description": "Get all holdings for a specific portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["portfolio_id"]
                }
            }
        }
