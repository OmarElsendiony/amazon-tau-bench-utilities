import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRoomsInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str = None,
               home_id: str = None) -> str:
        rooms = data.get("rooms", {})
        results = []

        for r in rooms.values():
            if room_id and r.get("room_id") != room_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue

            results.append({
                "room_id":       r.get("room_id"),
                "home_id":       r.get("home_id"),
                "room_type":     r.get("room_type"),
                "room_owner_id": r.get("room_owner_id"),
                "status":        r.get("status"),
                "width_ft":      r.get("width_ft"),
                "length_ft":     r.get("length_ft")
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_rooms_info",
                "description": "Retrieve room records filtered by optional room_id or home_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id":  {"type": "string"},
                        "home_id":  {"type": "string"}
                    },
                    "required": []
                }
            }
        }
