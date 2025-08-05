import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchInstrumentsWithItsPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: Optional[str] = None, name: Optional[str] = None,
               instrument_type: Optional[str] = None, date: Optional[str] = None,
               price_id: Optional[str] = None, open_price: Optional[float] = None,
               close_price: Optional[float] = None, high_price: Optional[float] = None,
               low_price: Optional[float] = None) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        results = []
        
        for instrument in instruments.values():
            if ticker and instrument.get("ticker") != ticker:
                continue
            if name and name.lower() not in instrument.get("name", "").lower():
                continue
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            
            # Get prices for this instrument
            instrument_prices = []
            for price in prices.values():
                if price.get("instrument_id") != instrument.get("instrument_id"):
                    continue
                if date and price.get("price_date") != date:
                    continue
                if price_id and price.get("price_id") != price_id:
                    continue
                if open_price is not None and price.get("open_price") != open_price:
                    continue
                if close_price is not None and price.get("close_price") != close_price:
                    continue
                if high_price is not None and price.get("high_price") != high_price:
                    continue
                if low_price is not None and price.get("low_price") != low_price:
                    continue
                instrument_prices.append(price)
            
            instrument_with_prices = instrument.copy()
            instrument_with_prices["prices"] = instrument_prices
            results.append(instrument_with_prices)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_instruments_with_its_price",
                "description": "Fetch instruments with their price information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Instrument ticker"},
                        "name": {"type": "string", "description": "Instrument name (partial match)"},
                        "instrument_type": {"type": "string", "description": "Instrument type (stock, bond, derivative, cash, other)"},
                        "date": {"type": "string", "description": "Price date"},
                        "price_id": {"type": "string", "description": "Price record ID"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "close_price": {"type": "number", "description": "Closing price"},
                        "high_price": {"type": "number", "description": "High price"},
                        "low_price": {"type": "number", "description": "Low price"}
                    },
                    "required": []
                }
            }
        }
