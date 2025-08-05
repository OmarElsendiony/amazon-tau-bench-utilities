import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class PurchaseInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, instrument_id: str, 
               quantity: str, cost_basis: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        portfolios = data.get("portfolios", {})
        instruments = data.get("instruments", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        holding_id = generate_id(portfolio_holdings)
        timestamp = "2025-10-01T00:00:00"
        
        new_holding = {
            "holding_id": holding_id,
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "quantity": quantity,
            "cost_basis": cost_basis,
            "created_at": timestamp
        }
        
        portfolio_holdings[str(holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "purchase_instrument",
                "description": "Purchase an instrument and add it to a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument to purchase"},
                        "quantity": {"type": "string", "description": "Quantity of the instrument to purchase"},
                        "cost_basis": {"type": "string", "description": "Cost basis per unit of the instrument"}
                    },
                    "required": ["portfolio_id", "instrument_id", "quantity", "cost_basis"]
                }
            }
        }
