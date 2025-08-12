import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDeviceDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               room_id: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               width_ft: Optional[float] = None,
               length_ft: Optional[float] = None,
               scheduled_maintainance_date: Optional[str] = None,
               last_maintainance_date: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None,
               resolution: Optional[str] = None,
               last_activity_timestamp: Optional[str] = None) -> str:
        
        devices = data.get("devices", {})
        cameras = data.get("security_cameras", {})
        timestamp = "2025-10-01T00:00:00"

        device = devices.get(device_id)
        if not device:
            return json.dumps({"success": False, "error": f"Device ID {device_id} not found"})

        # Update general device fields
        if room_id is not None:
            device["room_id"] = room_id
        if insurance_expiry_date is not None:
            device["insurance_expiry_date"] = insurance_expiry_date
        if home_id is not None:
            device["home_id"] = home_id
        if status is not None:
            device["status"] = status
        if width_ft is not None:
            device["width_ft"] = width_ft
        if length_ft is not None:
            device["length_ft"] = length_ft
        if scheduled_maintainance_date is not None:
            device["scheduled_maintainance_date"] = scheduled_maintainance_date
        if last_maintainance_date is not None:
            device["last_maintainance_date"] = last_maintainance_date
        if daily_rated_power_consumption_kWh is not None:
            device["daily_rated_power_consumption_kWh"] = daily_rated_power_consumption_kWh

        device["updated_at"] = timestamp
        result = {
            "device_id": device["device_id"],
            "device_type": device.get("device_type"),
            "room_id": device.get("room_id"),
            "home_id": device.get("home_id"),
            "status": device.get("status"),
            "width_ft": device.get("width_ft"),
            "length_ft": device.get("length_ft"),
            "price": device.get("price"),
            "daily_rated_power_consumption_kWh": device.get("daily_rated_power_consumption_kWh")
        }

        # If device is a camera, update resolution and activity timestamp
        if device.get("device_type") == "camera":
            camera = cameras.get(device_id)
            if camera:
                if resolution is not None:
                    camera["resolution"] = resolution
                if last_activity_timestamp is not None:
                    camera["last_activity_timestamp"] = last_activity_timestamp
                camera["updated_at"] = timestamp

                result["resolution"] = camera.get("resolution")
                result["last_activity_timestamp"] = camera.get("last_activity_timestamp")

        result["success"] = True
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_details",
                "description": "Update general device information. If the device is a camera, also update resolution and last activity timestamp.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "room_id": {"type": "string"},
                        "insurance_expiry_date": {"type": "string"},
                        "home_id": {"type": "string"},
                        "status": {"type": "string"},
                        "width_ft": {"type": "number"},
                        "length_ft": {"type": "number"},
                        "scheduled_maintainance_date": {"type": "string"},
                        "last_maintainance_date": {"type": "string"},
                        "daily_rated_power_consumption_kWh": {"type": "number"},
                        "resolution": {"type": "string"},
                        "last_activity_timestamp": {"type": "string"}
                    },
                    "required": ["device_id"]
                }
            }
        }
