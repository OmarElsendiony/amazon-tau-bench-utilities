import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchRoutine(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        routine_id: Optional[str] = None,
        user_id: Optional[str] = None,
        home_id: Optional[str] = None
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
            results.append(r)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_routine",
                "description": "Fetch routine(s) filtered by optional routine_id, user_id, or home_id.",
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
                        }
                    },
                    "required": []
                }
            }
        }
