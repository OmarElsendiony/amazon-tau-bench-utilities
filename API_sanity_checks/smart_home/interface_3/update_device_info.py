import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDeviceInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               device_type: Optional[str] = None,
               room_id: Optional[str] = None,
               installed_on: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None) -> str:
        """
        Update the basic information of a device (only from the 'devices' table).
        Only the provided fields will be updated. device_id is required.
        """

        devices = data.get("devices", {})
        timestamp = "2025-10-01T00:00:00"

        device = devices.get(device_id)
        if not device:
            return json.dumps({"success": False, "error": f"Device ID {device_id} not found"})

        # Update only the fields that are provided
        if device_type is not None:
            device["device_type"] = device_type
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
        if daily_rated_power_consumption_kWh is not None:
            device["daily_rated_power_consumption_kWh"] = daily_rated_power_consumption_kWh

        device["updated_at"] = timestamp

        return json.dumps({
            "success": True,
            "device_id": device_id,
            "updated_fields": {k: v for k, v in device.items() if k != "created_at"}
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_info",
                "description": "Update a device record in the 'devices' table using any of the optional fields. Only device_id is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device to update"},
                        "device_type": {"type": "string", "description": "Type of the device"},
                        "room_id": {"type": "string", "description": "Room ID where the device is located"},
                        "installed_on": {"type": "string", "description": "Installation date of the device"},
                        "insurance_expiry_date": {"type": "string", "description": "Insurance expiry date"},
                        "home_id": {"type": "string", "description": "Home ID where the device belongs"},
                        "status": {"type": "string", "description": "Device status (e.g., on/off)"},
                        "daily_rated_power_consumption_kWh": {
                            "type": "number",
                            "description": "Rated daily power consumption in kWh"
                        }
                    },
                    "required": ["device_id"]
                }
            }
        }
