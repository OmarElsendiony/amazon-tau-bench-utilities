import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class list_children(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               parent_id: str) -> str:

        results = [
            u for u in data.get("users", {}).values()
            if u.get("parent_id") == parent_id
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_children",
                "description": "Lists all users whose parent_id matches the given one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string", "description": "User ID of the parent"}
                    },
                    "required": ["parent_id"]
                }
            }
        }
