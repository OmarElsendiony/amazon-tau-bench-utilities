import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_portfolio_status_by_date(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, date: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        instrument_prices = data.get("instrument_prices", {})
        
        total_value = 0.0
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") != portfolio_id:
                continue
            
            instrument_id = holding.get("instrument_id")
            quantity = float(holding.get("quantity", 0))
            
            # Find the price for the given date
            price = None
            for price_record in instrument_prices.values():
                if (price_record.get("instrument_id") == instrument_id and 
                    price_record.get("price_date") == date):
                    price = float(price_record.get("close_price", 0))
                    break
            
            if price is not None:
                total_value += quantity * price
        
        return json.dumps({"portfolio_value": round(total_value, 2)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_status_by_date",
                "description": "Get portfolio value for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["portfolio_id", "date"]
                }
            }
        }
