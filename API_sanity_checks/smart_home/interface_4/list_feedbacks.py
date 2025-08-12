import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class ListFeedbacks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: Optional[str] = None,
               device_id: Optional[str] = None) -> str:
        
        feedbacks = data.get("user_feedbacks", {})
        results: List[Dict[str, Any]] = []

        for feedback in feedbacks.values():
            if user_id and str(feedback.get("user_id")) != user_id:
                continue
            if device_id and str(feedback.get("device_id")) != device_id:
                continue
            results.append(feedback)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_feedbacks",
                "description": "List user feedback records filtered optionally by user_id or device_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Filter feedbacks by user ID (optional)"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Filter feedbacks by device ID (optional)"
                        }
                    },
                    "required": []
                }
            }
        }
