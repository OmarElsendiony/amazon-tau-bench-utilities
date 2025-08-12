import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetHomeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               owner_id: Optional[str] = None) -> str:
        """Returns detailed info about the first home matching filters, including number of residents and occupied rooms."""

        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})

        home = next(
            (h for h in homes.values()
             if (not home_id or h.get("home_id") == home_id) and
                (not owner_id or h.get("owner_id") == owner_id)),
            None
        )

        if not home:
            return json.dumps({"error": "No matching home found"})

        num_residents = sum(
            1 for u in users.values()
            if u.get("primary_address_id") == home.get("address_id")
        )

        num_rooms_occupied = sum(
            1 for r in rooms.values()
            if r.get("home_id") == home.get("home_id") and r.get("status") == "occupied"
        )

        result = {
            "home_id":             home.get("home_id"),
            "owner_id":            home.get("owner_id"),
            "address_id":          home.get("address_id"),
            "home_type":           home.get("home_type"),
            "num_residents":       num_residents,
            "num_rooms_occupied":  num_rooms_occupied
        }

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_home_details",
                "description": "Returns detailed info about the first home matching optional filters (home_id, owner_id), including residents and occupied rooms.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "Unique ID of the home (optional)"
                        },
                        "owner_id": {
                            "type": "string",
                            "description": "ID of the home owner (optional)"
                        }
                    },
                    "required": []
                }
            }
        }
