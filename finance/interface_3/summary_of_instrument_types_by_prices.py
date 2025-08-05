import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SummaryOfInstrumentTypesByPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], date: str) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Group instruments by type
        instrument_types = {}
        for instrument in instruments.values():
            inst_type = instrument.get("instrument_type")
            if inst_type not in instrument_types:
                instrument_types[inst_type] = []
            instrument_types[inst_type].append(instrument.get("instrument_id"))
        
        # Find prices for the specific date
        date_prices = {}
        for price in prices.values():
            if price.get("price_date") == date:
                date_prices[str(price.get("instrument_id"))] = price
        
        # Create summary
        results = []
        for inst_type, instrument_ids in instrument_types.items():
            total_instruments = len(instrument_ids)
            instruments_with_prices = 0
            total_close_value = 0.0
            avg_close_price = 0.0
            
            for inst_id in instrument_ids:
                if str(inst_id) in date_prices:
                    instruments_with_prices += 1
                    total_close_value += float(date_prices[str(inst_id)].get("close_price", 0))
            
            if instruments_with_prices > 0:
                avg_close_price = total_close_value / instruments_with_prices
            
            summary = {
                "instrument_type": inst_type,
                "total_instruments": total_instruments,
                "instruments_with_prices": instruments_with_prices,
                "average_close_price": round(avg_close_price, 4),
                "total_close_value": round(total_close_value, 2),
                "date": date
            }
            results.append(summary)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "summary_of_instrument_types_by_prices",
                "description": "Get summary of instrument types with pricing data for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "Date for price summary (YYYY-MM-DD format)"}
                    },
                    "required": ["date"]
                }
            }
        }
