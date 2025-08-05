import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_energy_tariffs_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str) -> str:

        results = []
        for t in data.get("energy_tariffs", {}).values():
            if t.get("home_id") == home_id:
                results.append(t)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_energy_tariffs_info",
                "description": "Fetches all energy tariff records for the given home ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Home ID"}
                    },
                    "required": ["home_id"]
                }
            }
        }
