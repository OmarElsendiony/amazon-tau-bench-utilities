import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateAddress(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               house_number: str,
               building_name: str,
               street: str,
               city_name: str,
               state: str) -> str:
        
        addresses = data.setdefault("addresses", {})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        address_id = generate_id(addresses)
        timestamp = "2025-10-01T00:00:00"

        new_address = {
            "address_id": address_id,
            "house_number": house_number,
            "building_name": building_name,
            "street": street,
            "city_name": city_name,
            "state": state,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        addresses[address_id] = new_address
        return json.dumps({"address_id": address_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_address",
                "description": "Create a new address record.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "house_number": {"type": "string", "description": "House number"},
                        "building_name": {"type": "string", "description": "Building name"},
                        "street": {"type": "string", "description": "Street name"},
                        "city_name": {"type": "string", "description": "City name"},
                        "state": {"type": "string", "description": "State"}
                    },
                    "required": ["house_number", "building_name", "street", "city_name", "state"]
                }
            }
        }
