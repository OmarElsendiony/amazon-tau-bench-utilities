import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AverageRatingDevice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], device_id: str) -> str:
        """
        Compute the average rating for the specified device based on user feedback.
        """
        feedbacks = data.get("user_feedbacks", {})
        total_rating = 0
        count = 0

        for feedback in feedbacks.values():
            if str(feedback.get("device_id")) == device_id:
                total_rating += feedback.get("rating", 0)
                count += 1

        average = round(total_rating / count, 2) if count > 0 else 0.0

        return json.dumps({"average_rating": average})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "average_rating_device",
                "description": "Calculate the average rating for a given device based on user feedback.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "ID of the device to calculate average rating for"
                        }
                    },
                    "required": ["device_id"]
                }
            }
        }
