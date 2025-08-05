import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str,
               trade_date: str, quantity: float, price: float, side: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument with ID {instrument_id} not found")
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side not in valid_sides:
            raise ValueError(f"Invalid side. Must be one of {valid_sides}")
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": str(trade_id),
            "fund_id": str(fund_id),
            "instrument_id": str(instrument_id),
            "trade_date": trade_date,
            "quantity": quantity,
            "price": price,
            "side": side,
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        return json.dumps(new_trade)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_trade_for_fund",
                "description": "Add a new trade for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "trade_date": {"type": "string", "description": "Trade date in ISO format"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"}
                    },
                    "required": ["fund_id", "instrument_id", "trade_date", "quantity", "price", "side"]
                }
            }
        }
