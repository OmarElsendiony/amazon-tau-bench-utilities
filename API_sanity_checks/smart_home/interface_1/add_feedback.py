import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddFeedback(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               device_id: str,
               rating: int) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00"
        feedbacks = data.setdefault("user_feedbacks", {})
        feedback_id = generate_id(feedbacks)

        feedbacks[feedback_id] = {
            "user_feedback_id": feedback_id,
            "user_id": user_id,
            "device_id": device_id,
            "rating": rating,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        return json.dumps({"user_feedback_id": feedback_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_feedback",
                "description": "Add feedback from a user for a device with a rating.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user providing the feedback"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "ID of the device being rated"
                        },
                        "rating": {
                            "type": "integer",
                            "description": "Rating given to the device (typically 1 to 5)"
                        }
                    },
                    "required": ["user_id", "device_id", "rating"]
                }
            }
        }
