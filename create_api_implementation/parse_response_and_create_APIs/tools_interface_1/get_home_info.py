import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_home_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               owner_id: Optional[str] = None,
               address_id: Optional[str] = None) -> str:

        results = []
        homes = data.get("homes", {})
        rooms = data.get("rooms", {})

        for h in homes.values():
            if home_id and h.get("home_id") != home_id:
                continue
            if owner_id and h.get("owner_id") != owner_id:
                continue
            if address_id and h.get("address_id") != address_id:
                continue

            # Compute stats
            residents = {
                room.get("room_owner_id")
                for room in rooms.values()
                if room.get("home_id") == h.get("home_id") and room.get("room_owner_id")
            }
            occupied = sum(
                1 for room in rooms.values()
                if room.get("home_id") == h.get("home_id") and room.get("status") == "occupied"
            )

            rec = h.copy()
            rec["num_residents"] = len(residents)
            rec["num_rooms_occupied"] = occupied
            results.append(rec)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_home_info",
                "description": "Retrieves home info with resident and room occupancy stats",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "owner_id": {"type": "string", "description": "Filter by owner ID"},
                        "address_id": {"type": "string", "description": "Filter by address ID"}
                    },
                    "required": []
                }
            }
        }
