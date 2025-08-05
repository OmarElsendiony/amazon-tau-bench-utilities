import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class add_device(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               room_id: str,
               home_id: str,
               width_ft: float,
               length_ft: float,
               price: float,
               daily_rated_power_consumption_kWh: float,
               brightness_level: Optional[str] = None,
               color: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        devices = data.get("devices", {})
        device_id = generate_id(devices)
        timestamp = "2025-10-01T00:00:00ZZ"

        new_device = {
            "device_id": device_id,
            "device_type": device_type,
            "room_id": room_id,
            "home_id": home_id,
            "installed_on": timestamp,
            "insurance_expiry_date": insurance_expiry_date,
            "status": "off",
            "width_ft": width_ft,
            "length_ft": length_ft,
            "price": price,
            "scheduled_maintainance_date": None,
            "last_maintainance_date": None,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        devices[device_id] = new_device

        # If bulb, also create smart_bulb entry
        if device_type == "bulb":
            bulbs = data.get("smart_bulbs", {})
            bulbs[device_id] = {
                "device_id": device_id,
                "brightness_level": brightness_level,
                "color": color,
                "created_at": timestamp,
                "updated_at": timestamp
            }

        return json.dumps({"device_id": device_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_device",
                "description": "Adds a new device; if a bulb, also creates smart bulb entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {"type": "string", "description": "Type of device"},
                        "room_id": {"type": "string", "description": "Room ID"},
                        "home_id": {"type": "string", "description": "Home ID"},
                        "width_ft": {"type": "number", "description": "Width in feet"},
                        "length_ft": {"type": "number", "description": "Length in feet"},
                        "price": {"type": "number", "description": "Price"},
                        "daily_rated_power_consumption_kWh": {
                            "type": "number",
                            "description": "Daily power consumption"
                        },
                        "brightness_level": {
                            "type": "string",
                            "description": "Initial brightness (for bulb)"
                        },
                        "color": {"type": "string", "description": "Initial color (for bulb)"},
                        "insurance_expiry_date": {
                            "type": "string",
                            "description": "Insurance expiry date"
                        }
                    },
                    "required": [
                        "device_type",
                        "room_id",
                        "home_id",
                        "width_ft",
                        "length_ft",
                        "price",
                        "daily_rated_power_consumption_kWh"
                    ]
                }
            }
        }
