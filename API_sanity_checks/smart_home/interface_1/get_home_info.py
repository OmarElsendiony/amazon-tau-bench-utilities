import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetHomeInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str = None,
               owner_id: str = None,
               address_id: str = None) -> str:
        """Fetch homes filtered by home_id, owner_id, or address_id; include num_residents and num_rooms_occupied."""
        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})
        results = []

        for h in homes.values():
            if home_id and h.get("home_id") != home_id:
                continue
            if owner_id and h.get("owner_id") != owner_id:
                continue
            if address_id and h.get("address_id") != address_id:
                continue

            num_residents = sum(
                1 for u in users.values()
                if u.get("primary_address_id") == h.get("address_id")
            )

            num_rooms_occupied = sum(
                1 for r in rooms.values()
                if r.get("home_id") == h.get("home_id") and r.get("status") == "occupied"
            )

            results.append({
                "home_id":             h.get("home_id"),
                "owner_id":            h.get("owner_id"),
                "address_id":          h.get("address_id"),
                "home_type":           h.get("home_type"),
                "num_residents":       num_residents,
                "num_rooms_occupied":  num_rooms_occupied
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_home_info",
                "description": "Filter homes by optional home_id, owner_id, or address_id; returns num_residents and num_rooms_occupied.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id":    {"type": "string"},
                        "owner_id":   {"type": "string"},
                        "address_id": {"type": "string"}
                    },
                    "required": []
                }
            }
        }
