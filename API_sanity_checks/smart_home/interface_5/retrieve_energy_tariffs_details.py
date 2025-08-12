import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveEnergyTariffsDetails(Tool):
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
                "name": "retrieve_energy_tariffs_details",
                "description": "Retrieve all energy tariff records associated with a given home_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "ID of the home to retrieve energy tariffs for"
                        }
                    },
                    "required": ["home_id"]
                }
            }
        }
