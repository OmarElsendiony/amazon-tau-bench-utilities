import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class MarkUserInactive(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               new_status: str) -> str:
        """
        Mark a user as inactive (or any new status) by updating their status field.
        """
        users = data.get("users", {})
        user = users.get(user_id)

        if not user:
            return json.dumps({"error": f"User with ID {user_id} not found."})

        user["status"] = new_status
        user["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "mark_user_inactive",
                "description": "Update the status of a user (e.g., to mark them as inactive).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to update"
                        },
                        "new_status": {
                            "type": "string",
                            "description": "New status to assign to the user (e.g., 'inactive')"
                        }
                    },
                    "required": ["user_id", "new_status"]
                }
            }
        }
