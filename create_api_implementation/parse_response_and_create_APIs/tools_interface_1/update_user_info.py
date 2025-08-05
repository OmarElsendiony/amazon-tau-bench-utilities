import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_user_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None,
               phone_number: Optional[str] = None,
               role: Optional[str] = None,
               email: Optional[str] = None,
               primary_address_id: Optional[str] = None) -> str:

        users = data.get("users", {})
        user = users.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        for field, val in [
            ("first_name", first_name),
            ("last_name", last_name),
            ("phone_number", phone_number),
            ("role", role),
            ("email", email),
            ("primary_address_id", primary_address_id)
        ]:
            if val is not None:
                user[field] = val

        user["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_info",
                "description": "Updates user record fields by user_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "first_name": {"type": "string", "description": "New first name"},
                        "last_name": {"type": "string", "description": "New last name"},
                        "phone_number": {"type": "string", "description": "New phone number"},
                        "role": {"type": "string", "description": "New role"},
                        "email": {"type": "string", "description": "New email"},
                        "primary_address_id": {"type": "string", "description": "New primary address ID"}
                    },
                    "required": ["user_id"]
                }
            }
        }
