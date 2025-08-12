import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveDeviceInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], device_id: str) -> str:
        """
        Retrieve full information for a specific device from the devices table using device_id.
        """
        devices = data.get("devices", {})
        device = devices.get(device_id)

        if not device:
            return json.dumps({"success": False, "error": f"Device with ID {device_id} not found."})

        return json.dumps(device)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_device_info",
                "description": "Retrieve full information for a specific device using device_id from the devices table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "The ID of the device to retrieve."
                        }
                    },
                    "required": ["device_id"]
                }
            }
        }
