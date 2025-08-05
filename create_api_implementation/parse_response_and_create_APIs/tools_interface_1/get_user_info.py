import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: Optional[str] = None,
               phone_number: Optional[str] = None,
               email: Optional[str] = None) -> str:

        results = []
        for u in data.get("users", {}).values():
            if user_id and u.get("user_id") != user_id:
                continue
            if phone_number and not u.get("phone_number", "").endswith(phone_number):
                continue
            if email and not u.get("email", "").lower().endswith(email.lower()):
                continue
            results.append(u)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Retrieves user records by user_id, phone, or email with case-insensitive/suffix matching",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "phone_number": {"type": "string", "description": "Filter by end of phone number"},
                        "email": {"type": "string", "description": "Filter by end of email address"}
                    },
                    "required": []
                }
            }
        }
