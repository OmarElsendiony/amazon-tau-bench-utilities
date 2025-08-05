import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        users = data.get("users", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for user in users.values():
            # Apply filters
            if filters.get("user_id") and str(user.get("user_id")) != str(filters["user_id"]):
                continue
            if filters.get("email") and user.get("email", "").lower() != filters["email"].lower():
                continue
            if filters.get("role") and user.get("role") != filters["role"]:
                continue
            if filters.get("status") and user.get("status") != filters["status"]:
                continue
            if filters.get("first_name") and filters["first_name"].lower() not in user.get("first_name", "").lower():
                continue
            if filters.get("last_name") and filters["last_name"].lower() not in user.get("last_name", "").lower():
                continue
                
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user",
                "description": "Find users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "user_id": {"type": "string", "description": "Filter by user ID"},
                                "email": {"type": "string", "description": "Filter by email address"},
                                "role": {"type": "string", "description": "Filter by role (admin, employee)"},
                                "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"},
                                "first_name": {"type": "string", "description": "Filter by first name (partial match)"},
                                "last_name": {"type": "string", "description": "Filter by last name (partial match)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
