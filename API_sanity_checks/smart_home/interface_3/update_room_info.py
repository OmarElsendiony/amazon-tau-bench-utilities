import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateRoomInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: str = None,
               status: str = None) -> str:
        
        rooms = data.get("rooms", {})
        room = rooms.get(str(room_id))
        if not room:
            raise ValueError(f"Room with ID {room_id} not found")

        timestamp = "2025-10-01T00:00:00"

        # Handle status change to vacant → clear owner
        if status == "vacant":
            room["status"] = "vacant"
            room["room_owner_id"] = None

        # Handle assigning owner to vacant room → auto-occupy
        elif room_owner_id is not None:
            room["room_owner_id"] = room_owner_id
            if room.get("status") == "vacant" and status is None:
                room["status"] = "occupied"

        # Update status if provided and not handled already
        if status is not None and status != "vacant":
            room["status"] = status

        room["updated_at"] = timestamp
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_info",
                "description": "Update room details like owner or status. Assigning an owner auto-occupies the room. Setting status to 'vacant' clears owner.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string"},
                        "room_owner_id": {"type": "string"},
                        "status": {"type": "string"}
                    },
                    "required": ["room_id"]
                }
            }
        }
