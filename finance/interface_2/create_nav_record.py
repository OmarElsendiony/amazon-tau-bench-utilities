import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNAVRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: str, 
               nav_value: float, currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_nav = {
            "nav_id": str(nav_id),
            "fund_id": str(fund_id),
            "nav_date": nav_date,
            "nav_value": nav_value,
            "currency": currency,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav
        return json.dumps(new_nav)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_nav_record",
                "description": "Create a new NAV record for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "nav_date": {"type": "string", "description": "NAV date in YYYY-MM-DD format"},
                        "nav_value": {"type": "number", "description": "NAV value"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["fund_id", "nav_date", "nav_value", "currency"]
                }
            }
        }
