import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveRoomInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str) -> str:
        """Fetch full details of a room by its ID."""

        rooms = data.get("rooms", {})
        room = rooms.get(room_id)

        if not room:
            return json.dumps({"error": f"Room with ID {room_id} not found"})

        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_room_info",
                "description": "Retrieve full details of a room using its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {
                            "type": "string",
                            "description": "Unique identifier of the room"
                        }
                    },
                    "required": ["room_id"]
                }
            }
        }
