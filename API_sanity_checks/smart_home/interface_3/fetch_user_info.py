import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FetchUserInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str = None,
               phone_number: str = None,
               email: str = None) -> str:
        """
        Retrieve users matching user_id, phone_number (suffix match), and/or email (case-insensitive).
        If no parameters are provided, return all users.
        """
        users = data.get("users", {})
        results = []

        def normalize_phone(p) -> str:
            return re.sub(r"\D", "", str(p or ""))

        target_phone = normalize_phone(phone_number)
        target_email = email.lower() if email else None

        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if target_phone:
                user_phone = normalize_phone(user.get("phone_number"))
                if not user_phone.endswith(target_phone):
                    continue
            if target_email:
                user_email = user.get("email", "").lower()
                if user_email != target_email:
                    continue
            results.append(user)

        return json.dumps(results if results else {"error": "No matching users found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Metadata for the fetch_user_info tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "fetch_user_info",
                "description": "Retrieve users based on user_id, phone_number, or email. Phone numbers are normalized and matched by suffix. Emails are case-insensitive.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Optional user ID to match"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Optional phone number to match (digits only, suffix match supported)"
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
