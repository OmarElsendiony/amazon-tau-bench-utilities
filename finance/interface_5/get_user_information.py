import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserInformation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user = users[str(user_id)]
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_information",
                "description": "Retrieve information for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to retrieve"}
                    },
                    "required": ["user_id"]
                }
            }
        }
