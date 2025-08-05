import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_rooms_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: Optional[str] = None,
               home_id: Optional[str] = None) -> str:

        results = []
        for r in data.get("rooms", {}).values():
            if room_id and r.get("room_id") != room_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue
            results.append(r)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_rooms_info",
                "description": "Fetches room records filtered by room_id or home_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string", "description": "Filter by room ID"},
                        "home_id": {"type": "string", "description": "Filter by home ID"}
                    },
                    "required": []
                }
            }
        }
