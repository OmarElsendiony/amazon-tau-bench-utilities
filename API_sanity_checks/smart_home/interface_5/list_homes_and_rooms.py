import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListHomesAndRooms(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: str) -> str:
        """Returns a list of homes with detailed room information and total users."""

        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})

        matching_home = next(
            (h for h in homes.values()
             if h.get("home_id") == home_id and
                h.get("owner_id") == owner_id),
            None
        )

        if not matching_home:
            return json.dumps([])

        address_id = matching_home.get("address_id")

        total_users = sum(
            1 for u in users.values()
            if u.get("primary_address_id") == address_id
        )

        list_rooms: List[Dict[str, Any]] = [
            {
                "room_id": r.get("room_id"),
                "home_id": r.get("home_id"),
                "room_type": r.get("room_type"),
                "room_owner_id": r.get("room_owner_id"),
                "status": r.get("status"),
                "width_ft": r.get("width_ft"),
                "length_ft": r.get("length_ft")
            }
            for r in rooms.values()
            if r.get("home_id") == home_id
        ]

        result = [{
            "home_id": matching_home.get("home_id"),
            "owner_id": matching_home.get("owner_id"),
            "address_id": matching_home.get("address_id"),
            "home_type": matching_home.get("home_type"),
            "total_users": total_users,
            "list_rooms": list_rooms
        }]

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_homes_and_rooms",
                "description": "Lists a home and its rooms with details like room type, owner, status, and size. Also includes number of users living at the home's address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Home ID to filter by"},
                        "owner_id": {"type": "string", "description": "Owner ID of the home"}
                    },
                    "required": ["home_id", "owner_id"]
                }
            }
        }
