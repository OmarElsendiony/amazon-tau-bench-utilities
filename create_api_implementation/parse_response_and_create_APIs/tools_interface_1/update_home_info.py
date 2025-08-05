import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_home_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: Optional[str] = None,
               address_id: Optional[str] = None,
               home_type: Optional[str] = None) -> str:

        homes = data.get("homes", {})
        home = homes.get(home_id)
        if not home:
            raise ValueError(f"Home {home_id} not found")

        if owner_id is not None:
            home["owner_id"] = owner_id
        if address_id is not None:
            home["address_id"] = address_id
        if home_type is not None:
            home["home_type"] = home_type

        home["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(home)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_home_info",
                "description": "Updates a home’s owner, address, or type if provided",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "ID of the home"},
                        "owner_id": {"type": "string", "description": "New owner user ID"},
                        "address_id": {"type": "string", "description": "New address ID"},
                        "home_type": {"type": "string", "description": "New home type (Home, Apartment)"}
                    },
                    "required": ["home_id"]
                }
            }
        }
