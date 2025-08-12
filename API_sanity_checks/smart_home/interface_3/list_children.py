import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListChildren(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               parent_id: str) -> str:
        users = data.get("users", {})
        results = [u for u in users.values() if u.get("parent_id") == parent_id]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_children",
                "description": "List all users who have the given parent_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"}
                    },
                    "required": ["parent_id"]
                }
            }
        }
