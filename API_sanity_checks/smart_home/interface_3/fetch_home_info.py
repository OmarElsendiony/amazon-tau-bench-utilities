import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchHomeInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               owner_id: Optional[str] = None,
               address_id: Optional[str] = None) -> str:
        """Fetch the first home matching optional filters with total users and list of room IDs."""

        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})

        for h in homes.values():
            if home_id and h.get("home_id") != home_id:
                continue
            if owner_id and h.get("owner_id") != owner_id:
                continue
            if address_id and h.get("address_id") != address_id:
                continue

            # Found matching home
            matched_home = h
            matched_home_id = h.get("home_id")
            matched_address_id = h.get("address_id")
            break
        else:
            return json.dumps({"error": "No matching home found"})

        list_rooms = [
            {"room_id": r.get("room_id")}
            for r in rooms.values()
            if r.get("home_id") == matched_home_id
        ]

        result = {
            "home_id": matched_home_id,
            "owner_id": matched_home.get("owner_id"),
            "address_id": matched_address_id,
            "home_type": matched_home.get("home_type"),
            "list_rooms": list_rooms
        }

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_home_info",
                "description": "Fetch the first home that matches optional filters: home_id, owner_id, or address_id. Returns total users and list of room IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "ID of the home (optional)"
                        },
                        "owner_id": {
                            "type": "string",
                            "description": "ID of the owner (optional)"
                        },
                        "address_id": {
                            "type": "string",
                            "description": "ID of the address (optional)"
                        }
                    },
                    "required": []
                }
            }
        }
