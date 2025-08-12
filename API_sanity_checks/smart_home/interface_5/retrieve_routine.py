import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveRoutine(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        routine_id: Optional[str] = None,
        user_id: Optional[str] = None,
        home_id: Optional[str] = None,
        action_time: Optional[str] = None,
        start_action_date: Optional[str] = None,
        action_interval: Optional[str] = None
    ) -> str:
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
            if start_action_date and r.get("start_action_date") != start_action_date:
                continue
            if action_interval and r.get("action_interval") != action_interval:
                continue
            results.append(r)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_routine",
                "description": "Retrieve routines filtered by any combination of routine_id, user_id, home_id, action_time, start_action_date, or action_interval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {
                            "type": "string",
                            "description": "Routine ID to filter"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID to filter"
                        },
                        "home_id": {
                            "type": "string",
                            "description": "Home ID to filter"
                        },
                        "action_time": {
                            "type": "string",
                            "description": "Scheduled action time (e.g., '08:00')"
                        },
                        "start_action_date": {
                            "type": "string",
                            "description": "Start date of the routine (format: YYYY-MM-DD)"
                        },
                        "action_interval": {
                            "type": "string",
                            "description": "Interval at which routine should repeat (e.g., 'daily', 'weekly')"
                        }
                    },
                    "required": []
                }
            }
        }
