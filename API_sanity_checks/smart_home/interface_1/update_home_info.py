import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateHomeInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: str = None,
               address_id: str = None,
               home_type: str = None) -> str:
        
        homes = data.get("homes", {})
        home = homes.get(str(home_id))
        if not home:
            raise ValueError(f"Home with ID {home_id} not found")

        timestamp = "2025-10-01T00:00:00"
        if owner_id is not None:
            home["owner_id"] = owner_id
        if address_id is not None:
            home["address_id"] = address_id
        if home_type is not None:
            home["home_type"] = home_type

        home["updated_at"] = timestamp
        return json.dumps(home)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_home_info",
                "description": "Update home details like owner, address, or home type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string"},
                        "owner_id": {"type": "string"},
                        "address_id": {"type": "string"},
                        "home_type": {"type": "string"}
                    },
                    "required": ["home_id"]
                }
            }
        }
