import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchEnergyTariffsDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str) -> str:
        tariffs = data.get("energy_tariffs", {})
        results = [tariff for tariff in tariffs.values() if tariff.get("home_id") == home_id]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_energy_tariffs_details",
                "description": "Fetch all energy tariff records for a given home_id without filtering by date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "Home ID to fetch energy tariff records for"
                        }
                    },
                    "required": ["home_id"]
                }
            }
        }
