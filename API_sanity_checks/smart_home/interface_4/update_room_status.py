import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateRoomStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               status: str) -> str:
        """
        Update only the status of a room. If status is set to 'vacant', clears the room owner.
        """

        rooms = data.get("rooms", {})
        room = rooms.get(str(room_id))
        if not room:
            raise ValueError(f"Room with ID {room_id} not found")

        timestamp = "2025-10-01T00:00:00"

        # If vacant, clear the owner
        if status == "vacant":
            room["status"] = "vacant"
            room["room_owner_id"] = None
        else:
            room["status"] = status

        room["updated_at"] = timestamp
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_status",
                "description": "Update the status of a room. If set to 'vacant', the room owner is removed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string"},
                        "status": {"type": "string"}
                    },
                    "required": ["room_id", "status"]
                }
            }
        }
