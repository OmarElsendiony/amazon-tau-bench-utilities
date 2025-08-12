import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str = None,
               email: str = None) -> str:
        """
        Retrieve users matching user_id and/or email (case-insensitive).
        If neither is provided, return all users.
        """
        users = data.get("users", {})
        target_email = email.lower() if email else None
        results = []

        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if target_email and user.get("email", "").lower() != target_email:
                continue
            results.append(user)

        return json.dumps(results if results else {"error": "No matching users found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Metadata for the get_user_details tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "get_user_details",
                "description": "Retrieve users matching user_id and/or email (case-insensitive). Returns all users if no filter is provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Optional user ID to match"
                        },
                        "email": {
                            "type": "string",
                            "description": "Optional email address to match (case-insensitive)"
                        }
                    },
                    "required": []
                }
            }
        }
