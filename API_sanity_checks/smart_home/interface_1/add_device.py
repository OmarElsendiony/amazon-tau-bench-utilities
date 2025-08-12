import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddDevice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               room_id: str,
               home_id: str,
               width_ft: float,
               length_ft: float,
               price: float,
               daily_rated_power_consumption_kWh: float,
               brightness_level: str = None,
               color: str = None,
               insurance_expiry_date: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            return max([int(k) for k in table.keys()], default=0) + 1

        timestamp = "2025-10-01T00:00:00"
        devices = data.setdefault("devices", {})
        smart_bulbs = data.setdefault("smart_bulbs", {})

        device_id = generate_id(devices)

        # Build device entry
        new_device = {
            "device_id": str(device_id),
            "device_type": device_type,
            "room_id": room_id,
            "installed_on": timestamp,
            "insurance_expiry_date": insurance_expiry_date or "2026-10-01",
            "home_id": home_id,
            "status": "off",
            "width_ft": width_ft,
            "length_ft": length_ft,
            "price": price,
            "scheduled_maintainance_date": None,
            "last_maintainance_date": timestamp,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        devices[str(device_id)] = new_device

        # Add to smart_bulbs if device is a bulb
        if device_type == "bulb":
            smart_bulbs[str(device_id)] = {
                "device_id": str(device_id),
                "brightness_level": brightness_level,
                "color": color,
                "created_at": timestamp,
                "updated_at": timestamp
            }

        return json.dumps({"device_id": str(device_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_device",
                "description": "Add a new device. If it's a bulb, also creates a smart_bulb record.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {
                            "type": "string",
                            "description": "Type of the device (e.g., bulb)"
                        },
                        "room_id": {
                            "type": "string",
                            "description": "ID of the room where the device is installed"
                        },
                        "home_id": {
                            "type": "string",
                            "description": "ID of the home"
                        },
                        "width_ft": {
                            "type": "number",
                            "description": "Width of the device in feet"
                        },
                        "length_ft": {
                            "type": "number",
                            "description": "Length of the device in feet"
                        },
                        "price": {
                            "type": "number",
                            "description": "Price of the device"
                        },
                        "daily_rated_power_consumption_kWh": {
                            "type": "number",
                            "description": "Rated daily power consumption"
                        },
                        "brightness_level": {
                            "type": "string",
                            "description": "Brightness level (used only for bulbs)"
                        },
                        "color": {
                            "type": "string",
                            "description": "Color (used only for bulbs)"
                        },
                        "insurance_expiry_date": {
                            "type": "string",
                            "description": "Optional insurance expiry date. Defaults to 2026-10-01"
                        }
                    },
                    "required": [
                        "device_type", "room_id", "home_id", "width_ft",
                        "length_ft", "price", "daily_rated_power_consumption_kWh"
                    ]
                }
            }
        }
