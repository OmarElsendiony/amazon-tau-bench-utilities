import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               first_name: str,
               last_name: str,
               phone_number: str,
               role: str,
               parent_id: Optional[str],
               email: str,
               primary_address_id: str,
               date_of_birth: str) -> str:

        users = data.setdefault("users", {})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"

        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "role": role,
            "parent_id": parent_id,
            "email": email,
            "primary_address_id": primary_address_id,
            "date_of_birth": date_of_birth,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }

        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Creates a new user with role, address, contact info, and optionally a parent user if role is 'Child'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "First name of the user"},
                        "last_name": {"type": "string", "description": "Last name of the user"},
                        "phone_number": {"type": "string", "description": "Phone number of the user"},
                        "role": {
                            "type": "string",
                            "description": "Role of the user (Owner, Partner, Child, Guest, Servant)"
                        },
                        "parent_id": {
                            "type": ["string", "null"],
                            "description": "Parent user ID (required if role is Child)"
                        },
                        "email": {"type": "string", "description": "Email address of the user"},
                        "primary_address_id": {
                            "type": "string",
                            "description": "Address ID where user lives"
                        },
                        "date_of_birth": {
                            "type": "string",
                            "description": "Date of birth in YYYY-MM-DD format"
                        }
                    },
                    "required": [
                        "first_name", "last_name", "phone_number", "role",
                        "email", "primary_address_id", "date_of_birth"
                    ]
                }
            }
        }
