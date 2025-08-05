import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, 
               email: Optional[str] = None, first_name: Optional[str] = None, 
               last_name: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user",
                "description": "Get user details by ID, email, or name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"},
                        "email": {"type": "string", "description": "User email"},
                        "first_name": {"type": "string", "description": "User first name"},
                        "last_name": {"type": "string", "description": "User last name"}
                    },
                    "required": []
                }
            }
        }
