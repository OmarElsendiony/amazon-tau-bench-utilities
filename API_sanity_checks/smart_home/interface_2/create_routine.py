import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateRoutine(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: int,
               home_id: int,
               action_time: str,
               start_action_date: str,
               action_interval: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        routines = data.setdefault("automated_routines", {})
        routine_id = generate_id(routines)
        timestamp = "2025-10-01T00:00:00"

        new_routine = {
            "routine_id": routine_id,
            "user_id": str(user_id),
            "home_id": str(home_id),
            "action_time": action_time,
            "start_action_date": start_action_date,
            "action_interval": action_interval,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        routines[routine_id] = new_routine

        return json.dumps({
            "routine_id": routine_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_routine",
                "description": "Create a new automated routine for a user and home.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id":           {"type": "integer", "description": "User ID for whom the routine is created"},
                        "home_id":           {"type": "integer", "description": "Home ID where routine applies"},
                        "action_time":       {"type": "string", "description": "Time of day to perform the action"},
                        "start_action_date": {"type": "string", "description": "Start date for the routine"},
                        "action_interval":   {"type": "string", "description": "How often the routine runs (e.g., daily, weekly)"}
                    },
                    "required": ["user_id", "home_id", "action_time", "start_action_date", "action_interval"]
                }
            }
        }
