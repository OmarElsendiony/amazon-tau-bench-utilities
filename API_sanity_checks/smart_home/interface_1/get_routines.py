import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRoutines(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: str = None,
               user_id: str = None,
               home_id: str = None,
               action_time: str = None,
               action_interval: str = None,
               start_action_date: str = None) -> str:
        routines = data.get("automated_routines", {})
        results = []

        for r in routines.values():
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
                "description": "Fetch automated routines filtered by any combination of routine_id, user_id, home_id, action_time, action_interval, or start_action_date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id":         {"type": "string"},
                        "user_id":            {"type": "string"},
                        "home_id":            {"type": "string"},
                        "action_time":        {"type": "string"},
                        "action_interval":    {"type": "string"},
                        "start_action_date":  {"type": "string"}
                    },
                    "required": []
                }
            }
        }
