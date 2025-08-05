import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateNAVRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], nav_id: str, nav_value: float, currency: str) -> str:
        nav_records = data.get("nav_records", {})
        
        # Validate NAV record exists
        if str(nav_id) not in nav_records:
            raise ValueError(f"NAV record with ID {nav_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        # Update NAV record
        nav_records[str(nav_id)]["nav_value"] = nav_value
        nav_records[str(nav_id)]["currency"] = currency
        nav_records[str(nav_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(nav_records[str(nav_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_nav_records",
                "description": "Update an existing NAV record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "NAV record ID"},
                        "nav_value": {"type": "number", "description": "New NAV value"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["nav_id", "nav_value", "currency"]
                }
            }
        }
