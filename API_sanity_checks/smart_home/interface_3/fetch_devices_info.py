import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchDevicesInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str = None,
               room_id: str = None,
               device_type: str = None,
               status: str = None,
               less_than_width_ft: float = None,
               less_than_length_ft: float = None) -> str:
        """
        Filter devices based on given parameters. Returns a list of device metadata.
        """
        devices = data.get("devices", {})
        results = []

        for d in devices.values():
            if device_id and str(d.get("device_id")) != device_id:
                continue
            if room_id and d.get("room_id") != room_id:
                continue
            if device_type and d.get("device_type") != device_type:
                continue
            if status and d.get("status") != status:
                continue
            if less_than_width_ft is not None and d.get("width_ft") is not None:
                if float(d.get("width_ft")) >= less_than_width_ft:
                    continue
            if less_than_length_ft is not None and d.get("length_ft") is not None:
                if float(d.get("length_ft")) >= less_than_length_ft:
                    continue

            results.append({
                "device_id": d.get("device_id"),
                "device_type": d.get("device_type"),
                "room_id": d.get("room_id"),
                "installed_on": d.get("installed_on"),
                "insurance_expiry_date": d.get("insurance_expiry_date"),
                "home_id": d.get("home_id"),
                "status": d.get("status"),
                "width_ft": d.get("width_ft"),
                "length_ft": d.get("length_ft"),
                "price": d.get("price"),
                "scheduled_maintainance_date": d.get("scheduled_maintainance_date"),
                "last_maintainance_date": d.get("last_maintainance_date"),
                "daily_rated_power_consumption_kWh": d.get("daily_rated_power_consumption_kWh")
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_devices_info",
                "description": "Fetch devices using optional filters including size constraints.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "room_id": {"type": "string"},
                        "device_type": {"type": "string"},
                        "status": {"type": "string"},
                        "less_than_width_ft": {"type": "number"},
                        "less_than_length_ft": {"type": "number"}
                    },
                    "required": []
                }
            }
        }
