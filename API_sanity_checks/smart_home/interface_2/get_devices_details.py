import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDevicesDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str = None,
               home_id: str = None,
               device_type: str = None,
               status: str = None,
               scheduled_maintaince_date: str = None) -> str:
        devices = data.get("devices", {})
        thermostat_commands = data.get("thermostat_commands", {})
        results = []

        for d in devices.values():
            if device_id and str(d.get("device_id")) != device_id:
                continue
            if home_id and d.get("home_id") != home_id:
                continue
            if device_type and d.get("device_type") != device_type:
                continue
            if status and d.get("status") != status:
                continue
            if scheduled_maintaince_date and d.get("scheduled_maintainance_date") != scheduled_maintaince_date:
                continue

            record = {
                "device_id": d.get("device_id"),
                "device_type": d.get("device_type"),
                "room_id": d.get("room_id"),
                "home_id": d.get("home_id"),
                "status": d.get("status"),
                "width_ft": d.get("width_ft"),
                "length_ft": d.get("length_ft"),
                "price": d.get("price"),
                "daily_rated_power_consumption_kWh": d.get("daily_rated_power_consumption_kWh"),
                "current_temperate": None,
                "lowest_rated_temeprature": d.get("lowest_rated_temeprature"),
                "highest_rated_temeprature": d.get("highest_rated_temeprature"),
                "last_adjustment_time": None
            }

            if d.get("device_type") == "thermostat":
                thermostat = next(
                    (tc for tc in thermostat_commands.values()
                     if str(tc.get("device_id")) == str(d.get("device_id"))),
                    None
                )
                if thermostat:
                    record["current_temperate"] = thermostat.get("current_temperature")
                    record["last_adjustment_time"] = thermostat.get("updated_at")

            results.append(record)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_devices_details",
                "description": "Retrieve devices filtered by device_id, home_id, device_type, status, or scheduled_maintaince_date. Includes thermostat temperature details.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "home_id": {"type": "string"},
                        "device_type": {"type": "string"},
                        "status": {"type": "string"},
                        "scheduled_maintaince_date": {"type": "string"}
                    },
                    "required": []
                }
            }
        }
