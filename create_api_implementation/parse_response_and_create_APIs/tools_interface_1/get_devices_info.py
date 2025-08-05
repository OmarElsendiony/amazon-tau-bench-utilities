import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_devices_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: Optional[str] = None,
               room_id: Optional[str] = None,
               device_type: Optional[str] = None,
               status: Optional[str] = None) -> str:

        results = []
        for dev in data.get("devices", {}).values():
            if device_id and dev.get("device_id") != device_id:
                continue
            if room_id and dev.get("room_id") != room_id:
                continue
            if device_type and dev.get("device_type") != device_type:
                continue
            if status and dev.get("status") != status:
                continue

            rec = dev.copy()
            # If bulb, merge smart_bulb info
            if rec.get("device_type") == "bulb":
                bulb = data.get("smart_bulbs", {}).get(rec.get("device_id"), {})
                rec["brightness_level"] = bulb.get("brightness_level")
                rec["color"] = bulb.get("color")

            results.append(rec)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_devices_info",
                "description": "Retrieves device info based on filters; adds bulb info if applicable",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "Filter by device ID"},
                        "room_id": {"type": "string", "description": "Filter by room ID"},
                        "device_type": {"type": "string", "description": "Filter by device type"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
