import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ListDevices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               room_id: Optional[str] = None,
               device_type: Optional[str] = None,
               status: Optional[str] = None,
               less_than_width_ft: Optional[float] = None,
               less_than_length_ft: Optional[float] = None,
               price: Optional[float] = None) -> str:
        """
        Returns a list of device IDs filtered by optional parameters.
        """
        devices = data.get("devices", {})
        result = []

        for device in devices.values():
            if home_id and str(device.get("home_id")) != home_id:
                continue
            if room_id and str(device.get("room_id")) != room_id:
                continue
            if device_type and device.get("device_type") != device_type:
                continue
            if status and device.get("status") != status:
                continue
            if less_than_width_ft is not None and float(device.get("width_ft", 0)) >= less_than_width_ft:
                continue
            if less_than_length_ft is not None and float(device.get("length_ft", 0)) >= less_than_length_ft:
                continue
            if price is not None and float(device.get("price", 0)) != price:
                continue

            result.append({"device_id": str(device.get("device_id"))})

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_devices",
                "description": "List device IDs based on optional filters like home, room, device type, status, size, and price.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "Filter by home ID"
                        },
                        "room_id": {
                            "type": "string",
                            "description": "Filter by room ID"
                        },
                        "device_type": {
                            "type": "string",
                            "description": "Filter by device type"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by device status (on/off)"
                        },
                        "less_than_width_ft": {
                            "type": "number",
                            "description": "Filter devices with width less than this value"
                        },
                        "less_than_length_ft": {
                            "type": "number",
                            "description": "Filter devices with length less than this value"
                        },
                        "price": {
                            "type": "number",
                            "description": "Filter devices matching this price"
                        }
                    },
                    "required": []
                }
            }
        }
