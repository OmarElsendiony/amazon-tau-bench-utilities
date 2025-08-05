import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorPortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str, quantity: str, 
               cost_basis: str) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        # Update holding details
        holding = portfolio_holdings[str(holding_id)]
        holding["quantity"] = quantity
        holding["cost_basis"] = cost_basis
        
        return json.dumps(holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_portfolio_holding",
                "description": "Update quantity and cost basis of a portfolio holding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding"},
                        "quantity": {"type": "string", "description": "New quantity of the holding"},
                        "cost_basis": {"type": "string", "description": "New cost basis per unit of the holding"}
                    },
                    "required": ["holding_id", "quantity", "cost_basis"]
                }
            }
        }
