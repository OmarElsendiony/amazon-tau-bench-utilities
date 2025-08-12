import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               role: Optional[str] = None,
               parent_id: Optional[str] = None,
               email: Optional[str] = None,
               date_of_birth: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        user = users.get(user_id)

        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        if role is not None:
            user["role"] = role
        if parent_id is not None:
            user["parent_id"] = parent_id
        if email is not None:
            user["email"] = email
        if date_of_birth is not None:
            user["date_of_birth"] = date_of_birth
        if status is not None:
            user["status"] = status

        user["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_profile",
                "description": "Update user profile fields such as role, parent_id, email, date of birth, and status using user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "role": {"type": "string", "description": "Updated user role"},
                        "parent_id": {"type": "string", "description": "Updated parent user ID"},
                        "email": {"type": "string", "description": "Updated email address"},
                        "date_of_birth": {"type": "string", "description": "Updated date of birth"},
                        "status": {"type": "string", "description": "Updated user status"}
                    },
                    "required": ["user_id"]
                }
            }
        }
