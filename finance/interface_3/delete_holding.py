import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str) -> str:
        holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        deleted_holding = holdings[str(holding_id)]
        del holdings[str(holding_id)]
        
        return json.dumps(deleted_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_holding",
                "description": "Delete a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding to delete"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
