import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime

class RetrieveInstrumentPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        results = []
        for price in prices.values():
            if str(price.get("instrument_id")) != str(instrument_id):
                continue
                
            price_date = price.get("price_date")
            if price_date:
                # Filter by date range if provided
                if start_date and price_date < start_date:
                    continue
                if end_date and price_date > end_date:
                    continue
                    
            results.append(price)
        
        # Sort by date
        results.sort(key=lambda x: x.get("price_date", ""))
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instrument_prices",
                "description": "Retrieve price history for a specific instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "start_date": {"type": "string", "description": "Start date for price range (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for price range (YYYY-MM-DD format)"}
                    },
                    "required": ["instrument_id"]
                }
            }
        }
