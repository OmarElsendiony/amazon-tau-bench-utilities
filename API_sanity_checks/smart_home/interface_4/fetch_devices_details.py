import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchDevicesDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str = None,
               room_id: str = None,
               device_type: str = None,
               status: str = None,
               less_than_width_ft: float = None,
               less_than_length_ft: float = None,
               price: float = None) -> str:
        
        devices = data.get("devices", {})
        cameras = data.get("security_cameras", {})
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
            if price is not None and d.get("price") is not None:
                if float(d.get("price")) > price:
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
                "daily_rated_power_consumption_kWh": d.get("daily_rated_power_consumption_kWh"),
            }

            # Add security camera fields if device is a camera
            if d.get("device_type") == "camera":
                camera = cameras.get(str(d.get("device_id")), {})
                device_info["resolution"] = camera.get("resolution")
                device_info["last_activity_timestamp"] = camera.get("last_activity_timestamp")
            else:
                device_info["resolution"] = None
                device_info["last_activity_timestamp"] = None

            results.append(device_info)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_devices_details",
                "description": "Fetch detailed device info. Adds camera resolution/activity timestamp if applicable.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "room_id": {"type": "string"},
                        "device_type": {"type": "string"},
                        "status": {"type": "string"},
                        "less_than_width_ft": {"type": "number"},
                        "less_than_length_ft": {"type": "number"},
                        "price": {"type": "number"}
                    },
                    "required": []
                }
            }
        }
