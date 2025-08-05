import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], trade_id: str, quantity: float, 
               price: float, status: str) -> str:
        trades = data.get("trades", {})
        
        # Validate trade exists
        if str(trade_id) not in trades:
            raise ValueError(f"Trade with ID {trade_id} not found")
        
        # Validate status
        valid_statuses = ["executed", "pending", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update trade
        trades[str(trade_id)]["quantity"] = quantity
        trades[str(trade_id)]["price"] = price
        trades[str(trade_id)]["status"] = status
        
        return json.dumps(trades[str(trade_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_trade_for_fund",
                "description": "Update an existing trade",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string", "description": "Trade ID"},
                        "quantity": {"type": "number", "description": "Updated trade quantity"},
                        "price": {"type": "number", "description": "Updated trade price"},
                        "status": {"type": "string", "description": "Trade status (executed, pending, failed)"}
                    },
                    "required": ["trade_id", "quantity", "price", "status"]
                }
            }
        }
