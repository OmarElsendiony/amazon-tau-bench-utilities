import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateRoomDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        """
        Update room owner and/or status. If status is 'vacant', clears owner.
        If assigning an owner and status is not provided, status becomes 'occupied'.
        """
        rooms = data.get("rooms", {})
        room = rooms.get(str(room_id))
        if not room:
            raise ValueError(f"Room with ID {room_id} not found")

        timestamp = "2025-10-01T00:00:00"

        if status == "vacant":
            room["status"] = "vacant"
            room["room_owner_id"] = None
        else:
            if status is not None:
                room["status"] = status
            if room_owner_id is not None:
                room["room_owner_id"] = room_owner_id
                if status is None:
                    room["status"] = "occupied"

        room["updated_at"] = timestamp
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_details",
                "description": "Update the room's owner and/or status. If status is 'vacant', owner is removed. Otherwise, sets the given owner and/or status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {
                            "type": "string",
                            "description": "Room ID to update"
                        },
                        "room_owner_id": {
                            "type": "string",
                            "description": "New room owner ID (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New room status (optional)"
                        }
                    },
                    "required": ["room_id"]
                }
            }
        }
