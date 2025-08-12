import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateDevice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               room_id: str,
               insurance_expiry_date: str,
               home_id: str,
               status: str,
               width_ft: float,
               length_ft: float,
               price: float,
               daily_rated_power_consumption_kWh: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            return max([int(k) for k in table.keys()], default=0) + 1

        timestamp = "2025-10-01T00:00:00"
        devices = data.setdefault("devices", {})
        device_id = generate_id(devices)

        devices[str(device_id)] = {
            "device_id": str(device_id),
            "device_type": device_type,
            "room_id": room_id,
            "installed_on": timestamp,
            "insurance_expiry_date": insurance_expiry_date,
            "home_id": home_id,
            "status": status,
            "width_ft": width_ft,
            "length_ft": length_ft,
            "price": price,
            "scheduled_maintainance_date": None,
            "last_maintainance_date": timestamp,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        return json.dumps({"device_id": str(device_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_device",
                "description": "Create a new device entry. Only updates the devices table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {"type": "string", "description": "Type of the device (e.g., thermostat, bulb, etc.)"},
                        "room_id": {"type": "string", "description": "Room in which the device is placed"},
                        "insurance_expiry_date": {"type": "string", "description": "Date when insurance expires"},
                        "home_id": {"type": "string", "description": "Home to which the device belongs"},
                        "status": {"type": "string", "description": "Device status (on/off)"},
                        "width_ft": {"type": "number", "description": "Width in feet"},
                        "length_ft": {"type": "number", "description": "Length in feet"},
                        "price": {"type": "number", "description": "Price of the device"},
                        "daily_rated_power_consumption_kWh": {"type": "number", "description": "Rated daily power usage"}
                    },
                    "required": [
                        "device_type", "room_id", "insurance_expiry_date", "home_id", "status",
                        "width_ft", "length_ft", "price", "daily_rated_power_consumption_kWh"
                    ]
                }
            }
        }
