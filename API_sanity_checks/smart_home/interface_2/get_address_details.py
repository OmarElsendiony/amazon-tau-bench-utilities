import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAddressDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               house_number: str = None,
               building_name: str = None,
               street: str = None,
               city_name: str = None,
               state: str = None) -> str:
        """
        Retrieve addresses matching any combination of the provided fields.
        Returns a JSON array of matching address objects (including address_id).
        """
        addresses = data.get("addresses", {})
        results = []

        def norm(val: Any) -> str:
            return str(val).strip().lower()

        for addr in addresses.values():
            if house_number and norm(addr.get("house_number")) != norm(house_number):
                continue
            if building_name and norm(addr.get("building_name")) != norm(building_name):
                continue
            if street and norm(addr.get("street")) != norm(street):
                continue
            if city_name and norm(addr.get("city_name")) != norm(city_name):
                continue
            if state and norm(addr.get("state")) != norm(state):
                continue

            results.append({
                "address_id": addr.get("address_id"),
                "house_number": addr.get("house_number"),
                "building_name": addr.get("building_name"),
                "street": addr.get("street"),
                "city_name": addr.get("city_name"),
                "state": addr.get("state"),
                "created_at": addr.get("created_at"),
                "updated_at": addr.get("updated_at"),
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_address_details",
                "description": "Retrieve addresses matching any combination of the provided fields.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "house_number": {"type": "string", "description": "House number"},
                        "building_name": {"type": "string", "description": "Building name"},
                        "street": {"type": "string", "description": "Street name"},
                        "city_name": {"type": "string", "description": "City name"},
                        "state": {"type": "string", "description": "State name"}
                    },
                    "required": []
                }
            }
        }
