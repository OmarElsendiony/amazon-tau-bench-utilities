import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDeviceInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               room_id: Optional[str] = None,
               installed_on: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               width_ft: Optional[float] = None,
               length_ft: Optional[float] = None,
               price: Optional[float] = None,
               scheduled_maintainance_date: Optional[str] = None,
               last_maintainance_date: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None,
               brightness_level: Optional[str] = None,
               color: Optional[str] = None) -> str:
        """Update a device by ID. If bulb, update smart_bulbs if applicable and include brightness/color in output."""

        devices = data.get("devices", {})
        smart_bulbs = data.get("smart_bulbs", {})
        timestamp = "2025-10-01T00:00:00"

        device = devices.get(device_id)
        if not device:
            return json.dumps({"error": f"Device ID {device_id} not found"})

        # Update general device fields
        if room_id is not None:
            device["room_id"] = room_id
        if installed_on is not None:
            device["installed_on"] = installed_on
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
        if price is not None:
            device["price"] = price
        if scheduled_maintainance_date is not None:
            device["scheduled_maintainance_date"] = scheduled_maintainance_date
        if last_maintainance_date is not None:
            device["last_maintainance_date"] = last_maintainance_date
        if daily_rated_power_consumption_kWh is not None:
            device["daily_rated_power_consumption_kWh"] = daily_rated_power_consumption_kWh

        device["updated_at"] = timestamp

        # Prepare return data
        result = dict(device)

        # If bulb, update and include smart_bulb info
        if device.get("device_type") == "bulb":
            bulb = smart_bulbs.get(device_id)
            if bulb:
                if brightness_level is not None:
                    bulb["brightness_level"] = brightness_level
                if color is not None:
                    bulb["color"] = color
                bulb["updated_at"] = timestamp

                result["brightness_level"] = bulb.get("brightness_level")
                result["color"] = bulb.get("color")

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_info",
                "description": "Update a device by ID. If device is a bulb and brightness/color is provided, also update smart_bulbs and include them in the response.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "room_id": {"type": "string"},
                        "installed_on": {"type": "string"},
                        "insurance_expiry_date": {"type": "string"},
                        "home_id": {"type": "string"},
                        "status": {"type": "string"},
                        "width_ft": {"type": "number"},
                        "length_ft": {"type": "number"},
                        "price": {"type": "number"},
                        "scheduled_maintainance_date": {"type": "string"},
                        "last_maintainance_date": {"type": "string"},
                        "daily_rated_power_consumption_kWh": {"type": "number"},
                        "brightness_level": {"type": "string"},
                        "color": {"type": "string"}
                    },
                    "required": ["device_id"]
                }
            }
        }
