import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_address(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               house_number: str,
               building_name: str,
               street: str,
               city_name: str,
               state: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        addresses = data.get("addresses", {})
        addr_id = generate_id(addresses)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_addr = {
            "address_id": addr_id,
            "house_number": house_number,
            "building_name": building_name,
            "street": street,
            "city_name": city_name,
            "state": state,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        addresses[addr_id] = new_addr
        return json.dumps({"address_id": addr_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_address",
                "description": "Creates a new address entry in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "house_number": {"type": "string", "description": "House or unit number"},
                        "building_name": {"type": "string", "description": "Building name"},
                        "street": {"type": "string", "description": "Street name"},
                        "city_name": {"type": "string", "description": "City name"},
                        "state": {"type": "string", "description": "State name"}
                    },
                    "required": ["house_number", "building_name", "street", "city_name", "state"]
                }
            }
        }
