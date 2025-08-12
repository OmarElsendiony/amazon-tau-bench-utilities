import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetEnergyTariffsDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               effective_date: Optional[str] = None) -> str:
        tariffs = data.get("energy_tariffs", {})
        results = []

        for tariff in tariffs.values():
            if tariff.get("home_id") != home_id:
                continue

            if effective_date:
                start = tariff.get("effective_from")
                end = tariff.get("effective_until")  # may be null (ongoing)
                if not (start <= effective_date and (end is None or effective_date <= end)):
                    continue

            results.append(tariff)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_energy_tariffs_details",
                "description": "Return energy tariffs for a specific home. If effective_date is provided, only tariffs active on that date are returned.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "Home ID for which tariff details are requested"
                        },
                        "effective_date": {
                            "type": "string",
                            "description": "Optional date (YYYY-MM-DD) to filter tariffs effective on that day"
                        }
                    },
                    "required": ["home_id"]
                }
            }
        }
