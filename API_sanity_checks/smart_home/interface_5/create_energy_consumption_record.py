import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateEnergyConsumptionRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               home_id: str,
               room_id: str,
               date: str,
               power_used_kWh: float) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        records = data.setdefault("historical_energy_consumption", {})
        consumption_id = generate_id(records)
        timestamp = "2025-10-01T00:00:00"

        record = {
            "consumption_id": int(consumption_id),
            "device_id": int(device_id),
            "home_id": int(home_id),
            "room_id": int(room_id),
            "date": date,
            "power_used_kWh": power_used_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        records[consumption_id] = record

        return json.dumps({"consumption_id": consumption_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_energy_consumption_record",
                "description": "Create a new record of energy consumption for a specific device in a home and room on a given date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "ID of the device"
                        },
                        "home_id": {
                            "type": "string",
                            "description": "ID of the home"
                        },
                        "room_id": {
                            "type": "string",
                            "description": "ID of the room"
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of the energy usage record (YYYY-MM-DD)"
                        },
                        "power_used_kWh": {
                            "type": "number",
                            "description": "Power used in kilowatt-hours"
                        }
                    },
                    "required": ["device_id", "home_id", "room_id", "date", "power_used_kWh"]
                }
            }
        }
