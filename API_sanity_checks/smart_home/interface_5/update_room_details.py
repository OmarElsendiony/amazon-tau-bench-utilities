import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateRoomDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: str = None,
               status: str = None) -> str:
        """
        Update room owner and status. If status is 'vacant', clears owner.
        If assigning an owner, status becomes 'occupied' unless specified otherwise.
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
            if status:
                room["status"] = status
            if room_owner_id:
                room["room_owner_id"] = room_owner_id
                if not status:
                    room["status"] = "occupied"

        room["updated_at"] = timestamp
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_details",
                "description": "Update the room's owner and/or status. If status is 'vacant', owner is removed. If assigning an owner without status, defaults to 'occupied'.",
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
