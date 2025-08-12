import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FetchUserDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str = None,
               first_name: str = None,
               last_name: str = None,
               date_of_birth: str = None,
               phone_number: str = None,
               email: str = None) -> str:
        """
        Retrieve user records matching the provided filters. All parameters are optional.
        Phone numbers are normalized and matched by suffix. Email comparison is case-insensitive.
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
            if first_name and user.get("first_name") != first_name:
                continue
            if last_name and user.get("last_name") != last_name:
                continue
            if date_of_birth and user.get("date_of_birth") != date_of_birth:
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
        return {
            "type": "function",
            "function": {
                "name": "fetch_user_details",
                "description": "Fetch detailed user information by filtering on user_id, name, date of birth, phone number, or email. Phone numbers are normalized and suffix-matched. Email comparison is case-insensitive.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to match"},
                        "first_name": {"type": "string", "description": "First name of the user"},
                        "last_name": {"type": "string", "description": "Last name of the user"},
                        "date_of_birth": {"type": "string", "description": "Date of birth (YYYY-MM-DD)"},
                        "phone_number": {"type": "string", "description": "Phone number of the user (digits only, suffix match)"},
                        "email": {"type": "string", "description": "Email address (case-insensitive)"}
                    },
                    "required": []
                }
            }
        }
