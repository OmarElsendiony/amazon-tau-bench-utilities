import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundTradeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, start_date: Optional[str] = None,
               instrument_id: Optional[str] = None, quantity: Optional[float] = None,
               price: Optional[float] = None, side: Optional[str] = None,
               end_date: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        results = []
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            if instrument_id and trade.get("instrument_id") != instrument_id:
                continue
            if quantity is not None and trade.get("quantity") != quantity:
                continue
            if price is not None and trade.get("price") != price:
                continue
            if side and trade.get("side") != side:
                continue
            
            # Date filtering (assuming trade_date is in ISO format)
            trade_date = trade.get("trade_date", "")
            if start_date and trade_date < start_date:
                continue
            if end_date and trade_date > end_date:
                continue
            
            results.append(trade)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_trade_details",
                "description": "Get trade details for a specific fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "start_date": {"type": "string", "description": "Start date for filtering trades"},
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"},
                        "end_date": {"type": "string", "description": "End date for filtering trades"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
