import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str = None,
               phone_number: str = None,
               email: str = None) -> str:
        """
        Retrieve user records matching optional filters: user_id, phone_number, or email.
        Phone numbers are compared by digits only (ignoring formatting characters) and support suffix matching.
        Email comparisons are case-insensitive.
        """
        users = data.get("users", {})
        results = []

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(phone_number)
        target_email = email.lower() if email is not None else None

        for user in users.values():
            # Filter by user_id
            if user_id is not None and user.get("user_id") != user_id:
                continue

            # Filter by phone_number (normalize digits, allow suffix match)
            if target_phone:
                user_phone = normalize_phone(user.get("phone_number"))
                if not user_phone.endswith(target_phone):
                    continue

            # Filter by email (case-insensitive)
            if target_email:
                user_email = user.get("email", "").lower()
                if user_email != target_email:
                    continue

            results.append(user)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Metadata for the get_user_info tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Retrieve user records, filtered optionally by user_id, phone_number, or email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Filter by phone number; formatting characters are ignored; suffix match supported"
                        },
                        "email": {
                            "type": "string",
                            "description": "Filter by email address (case-insensitive)"
                        }
                    },
                    "required": []
                }
            }
        }
