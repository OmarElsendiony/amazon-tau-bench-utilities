import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDevicesInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str = None,
               room_id: str = None,
               device_type: str = None,
               status: str = None) -> str:
        devices = data.get("devices", {})
        smart_bulbs = data.get("smart_bulbs", {})
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

            device_info = {
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
            }

            if d.get("device_type") == "bulb":
                bulb_info = smart_bulbs.get(str(d.get("device_id")), {})
                device_info["brightness_level"] = bulb_info.get("brightness_level")
                device_info["color"] = bulb_info.get("color")

            results.append(device_info)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_devices_info",
                "description": "Retrieve devices filtered by device_id, room_id, device_type, or status. Adds brightness/color if the device is a bulb.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id":   {"type": "string"},
                        "room_id":     {"type": "string"},
                        "device_type": {"type": "string"},
                        "status":      {"type": "string"}
                    },
                    "required": []
                }
            }
        }
