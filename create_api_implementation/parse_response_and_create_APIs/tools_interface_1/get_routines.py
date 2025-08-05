import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_routines(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: Optional[str] = None,
               user_id: Optional[str] = None,
               home_id: Optional[str] = None,
               action_time: Optional[str] = None,
               action_interval: Optional[str] = None,
               start_action_date: Optional[str] = None) -> str:

        results = []
        for r in data.get("automated_routines", {}).values():
            if routine_id and r.get("routine_id") != routine_id:
                continue
            if user_id and r.get("user_id") != user_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue
            if action_time and r.get("action_time") != action_time:
                continue
            if action_interval and r.get("action_interval") != action_interval:
                continue
            if start_action_date and r.get("start_action_date") != start_action_date:
                continue
            results.append(r)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_routines",
                "description": "Retrieves automated routines based on various optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {"type": "string", "description": "Filter by routine ID"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "action_time": {"type": "string", "description": "Filter by action time"},
                        "action_interval": {"type": "string", "description": "Filter by interval"},
                        "start_action_date": {"type": "string", "description": "Filter by start date"}
                    },
                    "required": []
                }
            }
        }
