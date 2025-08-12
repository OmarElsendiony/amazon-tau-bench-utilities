import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateDeviceDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               device_type: Optional[str] = None,
               room_id: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               width_ft: Optional[float] = None,
               length_ft: Optional[float] = None,
               price: Optional[float] = None,
               scheduled_maintainance_date: Optional[str] = None,
               last_maintainance_date: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None,
               current_temperate: Optional[float] = None,
               lowest_rated_temeprature: Optional[float] = None,
               highest_rated_temeprature: Optional[float] = None,
               last_adjustment_time: Optional[str] = None) -> str:
        
        devices = data.get("devices", {})
        thermostats = data.get("smart_thermostats", {})
        timestamp = "2025-10-01T00:00:00"

        device = devices.get(device_id)
        if not device:
            return json.dumps({"error": f"Device ID {device_id} not found"})

        # Update general device fields
        if device_type is not None:
            device["device_type"] = device_type
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
        if price is not None:
            device["price"] = price
        if scheduled_maintainance_date is not None:
            device["scheduled_maintainance_date"] = scheduled_maintainance_date
        if last_maintainance_date is not None:
            device["last_maintainance_date"] = last_maintainance_date
        if daily_rated_power_consumption_kWh is not None:
            device["daily_rated_power_consumption_kWh"] = daily_rated_power_consumption_kWh
        device["updated_at"] = timestamp

        result = dict(device)

        # If thermostat, update and include smart_thermostat info
        if device.get("device_type") == "thermostat":
            thermo = thermostats.get(device_id)
            if thermo:
                if current_temperate is not None:
                    thermo["current_temperate"] = current_temperate
                if lowest_rated_temeprature is not None:
                    thermo["lowest_rated_temeprature"] = lowest_rated_temeprature
                if highest_rated_temeprature is not None:
                    thermo["highest_rated_temeprature"] = highest_rated_temeprature
                if last_adjustment_time is not None:
                    thermo["last_adjustment_time"] = last_adjustment_time
                thermo["updated_at"] = timestamp

                result.update({
                    "current_temperate": thermo.get("current_temperate"),
                    "lowest_rated_temeprature": thermo.get("lowest_rated_temeprature"),
                    "highest_rated_temeprature": thermo.get("highest_rated_temeprature"),
                    "last_adjustment_time": thermo.get("last_adjustment_time"),
                })

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_details",
                "description": "Update device information and thermostat-specific fields if applicable.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string"},
                        "device_type": {"type": "string"},
                        "room_id": {"type": "string"},
                        "insurance_expiry_date": {"type": "string"},
                        "home_id": {"type": "string"},
                        "status": {"type": "string"},
                        "width_ft": {"type": "number"},
                        "length_ft": {"type": "number"},
                        "price": {"type": "number"},
                        "scheduled_maintainance_date": {"type": "string"},
                        "last_maintainance_date": {"type": "string"},
                        "daily_rated_power_consumption_kWh": {"type": "number"},
                        "current_temperate": {"type": "number"},
                        "lowest_rated_temeprature": {"type": "number"},
                        "highest_rated_temeprature": {"type": "number"},
                        "last_adjustment_time": {"type": "string"}
                    },
                    "required": ["device_id"]
                }
            }
        }
