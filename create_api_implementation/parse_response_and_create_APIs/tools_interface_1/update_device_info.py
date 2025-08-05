import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_device_info(Tool):
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

        devices = data.get("devices", {})
        device = devices.get(device_id)
        if not device:
            raise ValueError(f"Device {device_id} not found")

        # Update main device fields
        for field, val in [
            ("room_id", room_id),
            ("installed_on", installed_on),
            ("insurance_expiry_date", insurance_expiry_date),
            ("home_id", home_id),
            ("status", status),
            ("width_ft", width_ft),
            ("length_ft", length_ft),
            ("price", price),
            ("scheduled_maintainance_date", scheduled_maintainance_date),
            ("last_maintainance_date", last_maintainance_date),
            ("daily_rated_power_consumption_kWh", daily_rated_power_consumption_kWh)
        ]:
            if val is not None:
                device[field] = val

        # Stamp update
        device["updated_at"] = "2025-10-01T00:00:00ZZ"

        # If bulb, update smart_bulbs record
        bulbs = data.get("smart_bulbs", {})
        if device_id in bulbs:
            bulb = bulbs[device_id]
            if brightness_level is not None:
                bulb["brightness_level"] = brightness_level
            if color is not None:
                bulb["color"] = color
            bulb["updated_at"] = "2025-10-01T00:00:00ZZ"

        return json.dumps(device)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_info",
                "description": "Updates a device’s attributes; also updates smart bulb info if applicable",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "room_id": {"type": "string", "description": "New room ID"},
                        "installed_on": {"type": "string", "description": "New install date"},
                        "insurance_expiry_date": {"type": "string", "description": "New insurance expiry date"},
                        "home_id": {"type": "string", "description": "New home ID"},
                        "status": {"type": "string", "description": "New status (on/off)"},
                        "width_ft": {"type": "number", "description": "New width in feet"},
                        "length_ft": {"type": "number", "description": "New length in feet"},
                        "price": {"type": "number", "description": "New price"},
                        "scheduled_maintainance_date": {"type": "string", "description": "New scheduled maintenance date"},
                        "last_maintainance_date": {"type": "string", "description": "New last maintenance date"},
                        "daily_rated_power_consumption_kWh": {"type": "number", "description": "New daily power consumption"},
                        "brightness_level": {"type": "string", "description": "New brightness level for bulb"},
                        "color": {"type": "string", "description": "New color for bulb"}
                    },
                    "required": ["device_id"]
                }
            }
        }
