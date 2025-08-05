import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_routine(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               home_id: str,
               action_time: str,
               start_action_date: str,
               action_interval: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        routines = data.get("automated_routines", {})
        routine_id = generate_id(routines)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_routine = {
            "routine_id": routine_id,
            "user_id": user_id,
            "home_id": home_id,
            "action_time": action_time,
            "start_action_date": start_action_date,
            "action_interval": action_interval,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        routines[routine_id] = new_routine
        return json.dumps({"routine_id": routine_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_routine",
                "description": "Creates a new automated routine for a user at a specific home",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"},
                        "home_id": {"type": "string", "description": "Home ID"},
                        "action_time": {"type": "string", "description": "Time to perform action (HH:MM:SS)"},
                        "start_action_date": {"type": "string", "description": "Date to start actions (YYYY-MM-DD)"},
                        "action_interval": {"type": "string", "description": "Interval (daily, one_time, every_hour)"}
                    },
                    "required": ["user_id", "home_id", "action_time", "start_action_date", "action_interval"]
                }
            }
        }
