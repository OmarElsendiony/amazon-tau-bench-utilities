import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class add_feedback(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               device_id: str,
               rating: int) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        feedbacks = data.get("user_feedbacks", {})
        fb_id = generate_id(feedbacks)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_fb = {
            "user_feedback_id": fb_id,
            "user_id": user_id,
            "device_id": device_id,
            "rating": rating,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        feedbacks[fb_id] = new_fb
        return json.dumps({"user_feedback_id": fb_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_feedback",
                "description": "Adds user feedback (rating) for a device",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "rating": {"type": "integer", "description": "Rating value"}
                    },
                    "required": ["user_id", "device_id", "rating"]
                }
            }
        }
