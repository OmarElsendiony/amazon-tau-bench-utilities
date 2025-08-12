import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUserInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None,
               phone_number: Optional[str] = None,
               role: Optional[str] = None,
               parent_id: Optional[str] = None,
               email: Optional[str] = None,
               primary_address_id: Optional[str] = None,
               date_of_birth: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        user = users.get(user_id)

        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        # Update fields if provided
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if phone_number is not None:
            user["phone_number"] = phone_number
        if role is not None:
            user["role"] = role
        if parent_id is not None:
            user["parent_id"] = parent_id
        if email is not None:
            user["email"] = email
        if primary_address_id is not None:
            user["primary_address_id"] = primary_address_id
        if date_of_birth is not None:
            user["date_of_birth"] = date_of_birth

        # Always update the timestamp
        user["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_info",
                "description": "Update user information by user_id. Updates only the fields provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "first_name": {"type": "string", "description": "Updated first name"},
                        "last_name": {"type": "string", "description": "Updated last name"},
                        "phone_number": {"type": "string", "description": "Updated phone number"},
                        "role": {"type": "string", "description": "Updated user role"},
                        "parent_id": {"type": "string", "description": "Updated parent ID"},
                        "email": {"type": "string", "description": "Updated email address"},
                        "primary_address_id": {"type": "string", "description": "Updated address ID"},
                        "date_of_birth": {"type": "string", "description": "Updated date of birth"}
                    },
                    "required": ["user_id"]
                }
            }
        }
