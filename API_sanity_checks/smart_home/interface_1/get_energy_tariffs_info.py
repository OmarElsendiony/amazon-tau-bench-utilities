import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetEnergyTariffsInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str) -> str:
        tariffs = data.get("energy_tariffs", {})
        results = [t for t in tariffs.values() if t.get("home_id") == home_id]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_energy_tariffs_info",
                "description": "Fetch all energy tariff records for a specific home_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string"}
                    },
                    "required": ["home_id"]
                }
            }
        }
