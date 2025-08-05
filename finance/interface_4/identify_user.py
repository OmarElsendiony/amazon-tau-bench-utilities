import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class IdentifyUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: Optional[str] = None, 
               user_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        if not email and not user_id:
            raise ValueError("Either email or user_id must be provided")
        
        for user in users.values():
            if email and user.get("email", "").lower() == email.lower():
                return json.dumps(user)
            if user_id and user.get("user_id") == user_id:
                return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "identify_user",
                "description": "Identify a user by email or user ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "User email address"},
                        "user_id": {"type": "string", "description": "User ID"}
                    },
                    "required": []
                }
            }
        }
