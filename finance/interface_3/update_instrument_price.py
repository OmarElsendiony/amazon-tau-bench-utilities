import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], price_id: str, open_price: Optional[str] = None, 
               high_price: Optional[str] = None, low_price: Optional[str] = None, 
               close_price: Optional[str] = None) -> str:
        prices = data.get("instrument_prices", {})
        
        # Validate price record exists
        if str(price_id) not in prices:
            raise ValueError(f"Price record {price_id} not found")
        
        price_record = prices[str(price_id)]
        
        # Update fields if provided
        if open_price is not None:
            price_record["open_price"] = open_price
        if high_price is not None:
            price_record["high_price"] = high_price
        if low_price is not None:
            price_record["low_price"] = low_price
        if close_price is not None:
            price_record["close_price"] = close_price
        
        return json.dumps(price_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update instrument price information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price_id": {"type": "string", "description": "ID of the price record"},
                        "open_price": {"type": "string", "description": "Opening price"},
                        "high_price": {"type": "string", "description": "High price"},
                        "low_price": {"type": "string", "description": "Low price"},
                        "close_price": {"type": "string", "description": "Closing price"}
                    },
                    "required": ["price_id"]
                }
            }
        }
