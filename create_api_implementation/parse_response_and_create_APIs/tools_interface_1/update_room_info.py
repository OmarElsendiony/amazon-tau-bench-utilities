import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_room_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: Optional[str] = None,
               status: Optional[str] = None) -> str:

        rooms = data.get("rooms", {})
        room = rooms.get(room_id)
        if not room:
            raise ValueError(f"Room {room_id} not found")

        # Assign owner and auto-occupy
        if room_owner_id is not None:
            room["room_owner_id"] = room_owner_id
            room["status"] = "occupied"

        # Update status if provided
        if status is not None:
            room["status"] = status

        room["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_info",
                "description": "Updates room owner or status; assigning owner auto-occupies room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string", "description": "ID of the room"},
                        "room_owner_id": {"type": "string", "description": "New owner user ID"},
                        "status": {"type": "string", "description": "New status (vacant, occupied)"}
                    },
                    "required": ["room_id"]
                }
            }
        }
