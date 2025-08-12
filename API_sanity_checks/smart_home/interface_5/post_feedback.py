import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class PostFeedback(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               device_id: str,
               rating: float) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

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

        return json.dumps({
            "user_feedback_id": feedback_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "post_feedback",
                "description": "Submit a user's feedback on a specific device with a rating.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user submitting the feedback"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "The ID of the device being rated"
                        },
                        "rating": {
                            "type": "number",
                            "description": "The feedback rating (e.g., from 1.0 to 5.0)"
                        }
                    },
                    "required": ["user_id", "device_id", "rating"]
                }
            }
        }
