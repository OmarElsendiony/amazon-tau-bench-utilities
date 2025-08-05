import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_instruments_prices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: Optional[str] = None,
               price_date: Optional[str] = None, ticker: Optional[str] = None) -> str:
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        results = []
        
        for price in instrument_prices.values():
            if instrument_id and price.get("instrument_id") != instrument_id:
                continue
            if price_date and price.get("price_date") != price_date:
                continue
            
            # If ticker filter is provided, need to check instrument data
            if ticker:
                instrument = None
                for inst in instruments.values():
                    if inst.get("instrument_id") == price.get("instrument_id"):
                        instrument = inst
                        break
                if not instrument or instrument.get("ticker", "").lower() != ticker.lower():
                    continue
            
            # Merge instrument data with price data
            instrument_with_price = dict(price)
            for inst in instruments.values():
                if inst.get("instrument_id") == price.get("instrument_id"):
                    instrument_with_price.update(inst)
                    break
            
            results.append(instrument_with_price)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments_prices",
                "description": "Get instrument prices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                        "price_date": {"type": "string", "description": "Filter by price date (YYYY-MM-DD)"},
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"}
                    },
                    "required": []
                }
            }
        }
