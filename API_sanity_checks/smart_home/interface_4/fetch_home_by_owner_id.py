import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class FetchHomeByOwnerId(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], owner_id: str) -> str:
        if not owner_id or not isinstance(owner_id, str):
            return json.dumps({"error": "owner_id (str) is required"})

        homes = data.get("homes", {}) or {}

        matched_homes: List[Dict[str, Any]] = [
            h for h in homes.values() if h.get("owner_id") == owner_id
        ]

        if not matched_homes:
            return json.dumps({"error": "No homes found for the given owner_id"})

        return json.dumps(matched_homes)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_home_by_owner_id",
                "description": "Fetch all homes from homes.json that belong to the given owner_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "owner_id": {
                            "type": "string",
                            "description": "Owner ID whose homes should be fetched"
                        }
                    },
                    "required": ["owner_id"]
                }
            }
        }
