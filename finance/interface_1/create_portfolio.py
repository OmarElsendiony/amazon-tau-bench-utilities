import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreatePortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, base_currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        portfolio_id = generate_id(portfolios)
        timestamp = "2025-10-01T00:00:00"
        
        new_portfolio = {
            "portfolio_id": portfolio_id,
            "investor_id": investor_id,
            "base_currency": base_currency,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        portfolios[str(portfolio_id)] = new_portfolio
        return json.dumps(new_portfolio)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_portfolio",
                "description": "Create a new portfolio for an investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "base_currency": {"type": "string", "description": "Base currency of the portfolio (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["investor_id", "base_currency"]
                }
            }
        }
