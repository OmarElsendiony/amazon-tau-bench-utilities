import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str,
               open_price: float, high_price: float, low_price: float, 
               close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument with ID {instrument_id} not found")
        
        # Check if price record exists for this instrument and date
        existing_price_id = None
        for price_id, price in instrument_prices.items():
            if (price.get("instrument_id") == str(instrument_id) and 
                price.get("price_date") == price_date):
                existing_price_id = price_id
                break
        
        if existing_price_id:
            # Update existing price record
            instrument_prices[existing_price_id]["open_price"] = open_price
            instrument_prices[existing_price_id]["high_price"] = high_price
            instrument_prices[existing_price_id]["low_price"] = low_price
            instrument_prices[existing_price_id]["close_price"] = close_price
            return json.dumps(instrument_prices[existing_price_id])
        else:
            # Create new price record
            price_id = generate_id(instrument_prices)
            new_price = {
                "price_id": str(price_id),
                "instrument_id": str(instrument_id),
                "price_date": price_date,
                "open_price": open_price,
                "high_price": high_price,
                "low_price": low_price,
                "close_price": close_price
            }
            instrument_prices[str(price_id)] = new_price
            return json.dumps(new_price)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update or create instrument price record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "price_date": {"type": "string", "description": "Price date in YYYY-MM-DD format"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "High price"},
                        "low_price": {"type": "number", "description": "Low price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
