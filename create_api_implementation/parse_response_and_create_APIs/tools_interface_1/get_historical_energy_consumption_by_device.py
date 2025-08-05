import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_historical_energy_consumption_by_device(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               date: Optional[str] = None,
               month: Optional[int] = None) -> str:

        total = 0.0
        for rec in data.get("historical_energy_consumption", {}).values():
            if rec.get("device_id") != device_id:
                continue
            rec_date = rec.get("date", "")
            if date and rec_date != date:
                continue
            if month:
                parts = rec_date.split("-")
                if len(parts) >= 2 and int(parts[1]) != month:
                    continue
            total += float(rec.get("power_used_kWh", 0))

        return json.dumps({"total_power_used_kWh": total})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_historical_energy_consumption_by_device",
                "description": "Returns device’s estimated energy usage using filters by date or month",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "date": {"type": "string", "description": "Filter by exact date (YYYY-MM-DD)"},
                        "month": {"type": "integer", "description": "Filter by month (1-12)"}
                    },
                    "required": ["device_id"]
                }
            }
        }
