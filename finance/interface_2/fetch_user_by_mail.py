import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchUserByMail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                return json.dumps(user)
        
        raise ValueError(f"User with email {email} not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_user_by_mail",
                "description": "Fetch a user by their email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address of the user"}
                    },
                    "required": ["email"]
                }
            }
        }
