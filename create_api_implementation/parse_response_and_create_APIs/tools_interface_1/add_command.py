import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class add_command(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               routine_id: str,
               device_id: str,
               device_status: str,
               bulb_brightness_level: Optional[str] = None,
               bulb_color: Optional[str] = None) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00ZZ"
        # Add generic device command
        device_commands = data.get("device_commands", {})
        cmd_id = generate_id(device_commands)
        new_cmd = {
            "device_command_id": cmd_id,
            "routine_id": routine_id,
            "device_id": device_id,
            "status": device_status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        device_commands[cmd_id] = new_cmd

        # If bulb, also add brightness/color
        if device_type == "bulb":
            bulb_commands = data.get("bulb_commands", {})
            bulb_cmd_id = generate_id(bulb_commands)
            new_bulb_cmd = {
                "bulb_command_id": bulb_cmd_id,
                "routine_id": routine_id,
                "device_id": device_id,
                "brightness_level": bulb_brightness_level,
                "color": bulb_color,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            bulb_commands[bulb_cmd_id] = new_bulb_cmd

        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_command",
                "description": "Adds a command to a device; if it's a bulb, adds brightness and color commands too",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {
                            "type": "string",
                            "description": "Type of device (camera, bulb, thermostat, speaker, tv, refrigerator, oven)"
                        },
                        "routine_id": {"type": "string", "description": "Routine ID"},
                        "device_id": {"type": "string", "description": "Device ID"},
                        "device_status": {"type": "string", "description": "Desired status (on/off)"},
                        "bulb_brightness_level": {
                            "type": "string",
                            "description": "Brightness level for bulb (dim, half, full)"
                        },
                        "bulb_color": {
                            "type": "string",
                            "description": "Color for bulb (red, white, yellow, blue)"
                        }
                    },
                    "required": ["device_type", "routine_id", "device_id", "device_status"]
                }
            }
        }
