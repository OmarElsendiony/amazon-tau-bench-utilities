import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_address(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               address_id: Optional[str] = None,
               house_number: Optional[str] = None,
               building_name: Optional[str] = None,
               street: Optional[str] = None,
               city_name: Optional[str] = None,
               state: Optional[str] = None) -> str:

        addresses = data.get("addresses", {})
        results = []

        for addr in addresses.values():
            if address_id and addr.get("address_id") != address_id:
                continue
            if house_number and addr.get("house_number", "").lower() != house_number.lower():
                continue
            if building_name and addr.get("building_name", "").lower() != building_name.lower():
                continue
            if street and addr.get("street", "").lower() != street.lower():
                continue
            if city_name and addr.get("city_name", "").lower() != city_name.lower():
                continue
            if state and addr.get("state", "").lower() != state.lower():
                continue
            results.append(addr)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_address",
                "description": "Retrieves address records matching the provided fields",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address_id": {"type": "string", "description": "Filter by address ID"},
                        "house_number": {"type": "string", "description": "Filter by house number"},
                        "building_name": {"type": "string", "description": "Filter by building name"},
                        "street": {"type": "string", "description": "Filter by street"},
                        "city_name": {"type": "string", "description": "Filter by city"},
                        "state": {"type": "string", "description": "Filter by state"}
                    },
                    "required": []
                }
            }
        }
