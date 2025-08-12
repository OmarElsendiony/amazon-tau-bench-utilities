import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateRoutine(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: str,
               user_id: str = None,
               home_id: str = None,
               action_time: str = None,
               start_action_date: str = None,
               action_interval: str = None) -> str:
        """
        Update fields of an existing routine based on routine_id.
        All other parameters are optional and only update if provided.
        """
        routines = data.get("automated_routines", {})
        routine = routines.get(str(routine_id))
        if not routine:
            raise ValueError(f"Routine with ID {routine_id} not found")

        timestamp = "2025-10-01T00:00:00"

        if user_id is not None:
            routine["user_id"] = user_id
        if home_id is not None:
            routine["home_id"] = home_id
        if action_time is not None:
            routine["action_time"] = action_time
        if start_action_date is not None:
            routine["start_action_date"] = start_action_date
        if action_interval is not None:
            routine["action_interval"] = action_interval

        routine["updated_at"] = timestamp

        return json.dumps(routine)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_routine",
                "description": "Update an existing automated routine by routine_id. All other fields are optional and only update if provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {"type": "string", "description": "ID of the routine to update"},
                        "user_id": {"type": "string", "description": "Updated user ID"},
                        "home_id": {"type": "string", "description": "Updated home ID"},
                        "action_time": {"type": "string", "description": "Updated time of day to perform the action"},
                        "start_action_date": {"type": "string", "description": "Updated start date for the routine"},
                        "action_interval": {"type": "string", "description": "Updated frequency (e.g., daily, weekly)"}
                    },
                    "required": ["routine_id"]
                }
            }
        }
