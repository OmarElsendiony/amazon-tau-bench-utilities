import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str, 
               open_price: float, high_price: float, low_price: float, close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate price logic
        if high_price < max(open_price, close_price, low_price):
            raise ValueError("High price must be >= open, close, and low prices")
        if low_price > min(open_price, close_price, high_price):
            raise ValueError("Low price must be <= open, close, and high prices")
        
        # Check if price already exists for this instrument and date
        for price in prices.values():
            if (str(price.get("instrument_id")) == str(instrument_id) and 
                price.get("price_date") == price_date):
                raise ValueError(f"Price already exists for instrument {instrument_id} on {price_date}")
        
        price_id = generate_id(prices)
        
        new_price = {
            "price_id": price_id,
            "instrument_id": instrument_id,
            "price_date": price_date,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "close_price": close_price
        }
        
        prices[str(price_id)] = new_price
        return json.dumps(new_price)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_instrument_price",
                "description": "Add new price data for an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "price_date": {"type": "string", "description": "Date of the price data (YYYY-MM-DD)"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "Highest price"},
                        "low_price": {"type": "number", "description": "Lowest price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
