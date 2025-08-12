import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListAddresses(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               address_id: str = None,
               city_name: str = None,
               building_name: str = None,
               street: str = None) -> str:
        """
        Retrieve addresses matching any combination of the provided optional fields.
        """
        addresses = data.get("addresses", {})
        results = []

        def norm(val: Any) -> str:
            return str(val).strip().lower()

        for addr in addresses.values():
            if address_id and str(addr.get("address_id")) != address_id:
                continue
            if building_name and norm(addr.get("building_name")) != norm(building_name):
                continue
            if street and norm(addr.get("street")) != norm(street):
                continue
            if city_name and norm(addr.get("city_name")) != norm(city_name):
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
                "name": "list_addresses",
                "description": "Retrieve a list of addresses filtered by optional parameters like address_id, building_name, street, and city_name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address_id": {
                            "type": "string",
                            "description": "Filter by address ID"
                        },
                        "building_name": {
                            "type": "string",
                            "description": "Filter by building name"
                        },
                        "street": {
                            "type": "string",
                            "description": "Filter by street name"
                        },
                        "city_name": {
                            "type": "string",
                            "description": "Filter by city name"
                        }
                    },
                    "required": []
                }
            }
        }
