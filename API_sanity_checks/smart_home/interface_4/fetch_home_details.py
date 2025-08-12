import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchHomeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: str) -> str:
        """Fetch detailed home info including users and rooms."""

        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})

        home = next(
            (h for h in homes.values()
             if h.get("home_id") == home_id and
                h.get("owner_id") == owner_id),
            None
        )

        if not home:
            return json.dumps({"error": "No matching home found"})

        address_id = home.get("address_id")
        total_users = sum(
            1 for u in users.values()
            if u.get("primary_address_id") == address_id
        )

        list_rooms = [
            {"room_id": r.get("room_id")}
            for r in rooms.values()
            if r.get("home_id") == home_id
        ]

        result = {
            "home_id": home_id,
            "owner_id": owner_id,
            "address_id": address_id,
            "home_type": home.get("home_type"),
            "total_users": total_users,
            "list_rooms": list_rooms
        }

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_home_details",
                "description": "Returns detailed information about a home, including address, home type, number of users, and room list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Home ID"},
                        "owner_id": {"type": "string", "description": "Owner ID of the home"}
                    },
                    "required": ["home_id", "owner_id"]
                }
            }
        }
