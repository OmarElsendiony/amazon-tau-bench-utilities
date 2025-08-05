import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RemoveHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        # Remove the holding
        del portfolio_holdings[str(holding_id)]
        
        return json.dumps({"holding_id": int(holding_id)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_holding",
                "description": "Remove a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding to remove"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
