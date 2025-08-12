import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRoomDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], room_id: str) -> str:
        """
        Return full details of the room matching the given room_id.
        """
        rooms = data.get("rooms", {})
        room = rooms.get(str(room_id))

        if not room:
            return json.dumps({"error": f"Room with ID {room_id} not found"})

        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_room_details",
                "description": "Returns all details of a specific room by room_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {
                            "type": "string",
                            "description": "The ID of the room to fetch"
                        }
                    },
                    "required": ["room_id"]
                }
            }
        }
