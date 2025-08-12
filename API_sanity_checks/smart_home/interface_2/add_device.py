import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddDevice(Tool):
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
               scheduled_maintainance_date: str,
               daily_rated_power_consumption_kWh: float,
               current_temperate: float = None,
               lowest_rated_temeprature: float = None,
               highest_rated_temeprature: float = None,
               last_adjustment_time: str = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            return max([int(k) for k in table.keys()], default=0) + 1

        timestamp = "2025-10-01T00:00:00"

        devices = data.setdefault("devices", {})
        smart_thermostats = data.setdefault("smart_thermostats", {})

        device_id = generate_id(devices)

        # Create device entry
        new_device = {
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
            "scheduled_maintainance_date": scheduled_maintainance_date,
            "last_maintainance_date": timestamp,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        devices[str(device_id)] = new_device

        # Add to smart_thermostats if applicable
        if device_type == "thermostat":
            smart_thermostats[str(device_id)] = {
                "device_id": str(device_id),
                "current_temperate": current_temperate,
                "lowest_rated_temeprature": lowest_rated_temeprature,
                "highest_rated_temeprature": highest_rated_temeprature,
                "last_adjustment_time": last_adjustment_time,
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
                "description": "Add a new device. If it's a thermostat, also creates a smart_thermostat record.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {"type": "string"},
                        "room_id": {"type": "string"},
                        "insurance_expiry_date": {"type": "string"},
                        "home_id": {"type": "string"},
                        "status": {"type": "string"},
                        "width_ft": {"type": "number"},
                        "length_ft": {"type": "number"},
                        "price": {"type": "number"},
                        "scheduled_maintainance_date": {"type": "string"},
                        "daily_rated_power_consumption_kWh": {"type": "number"},
                        "current_temperate": {"type": "number"},
                        "lowest_rated_temeprature": {"type": "number"},
                        "highest_rated_temeprature": {"type": "number"},
                        "last_adjustment_time": {"type": "string"}
                    },
                    "required": [
                        "device_type", "room_id", "insurance_expiry_date", "home_id", "status",
                        "width_ft", "length_ft", "price", "scheduled_maintainance_date",
                        "daily_rated_power_consumption_kWh"
                    ]
                }
            }
        }
