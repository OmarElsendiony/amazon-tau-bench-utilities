import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListRooms(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        home_id: Optional[str] = None,
        room_type: Optional[str] = None,
        owner_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        rooms = data.get("rooms", {})
        results = []

        for r in rooms.values():
            if home_id and r.get("home_id") != home_id:
                continue
            if room_type and r.get("room_type") != room_type:
                continue
            if owner_id and r.get("room_owner_id") != owner_id:
                continue
            if status and r.get("status") != status:
                continue

            results.append({
                "room_id":       r.get("room_id"),
                "home_id":       r.get("home_id"),
                "room_type":     r.get("room_type"),
                "room_owner_id": r.get("room_owner_id"),
                "status":        r.get("status"),
                "width_ft":      r.get("width_ft"),
                "length_ft":     r.get("length_ft"),
                "created_at":    r.get("created_at"),
                "updated_at":    r.get("updated_at")
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_rooms",
                "description": "List all room records optionally filtered by home_id, room_type, owner_id, and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id":   {"type": "string", "description": "Home ID to filter rooms"},
                        "room_type": {"type": "string", "description": "Room type (e.g., Bedroom, kitchen, lounge)"},
                        "owner_id":  {"type": "string", "description": "Room owner's user ID"},
                        "status":    {"type": "string", "description": "Occupancy status (vacant or occupied)"}
                    },
                    "required": []
                }
            }
        }
