import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddCommand(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               routine_id: str,
               device_id: str,
               device_status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00"

        # Insert into device_commands
        device_commands = data.setdefault("device_commands", {})
        dcid = generate_id(device_commands)
        device_commands[dcid] = {
            "device_command_id": dcid,
            "routine_id": routine_id,
            "device_id": device_id,
            "status": device_status,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        return json.dumps({"success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_command",
                "description": "Adds a device command entry for any device type to a routine.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {
                            "type": "string",
                            "description": "Type of the device (e.g., 'thermostat', 'bulb', etc.)"
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "ID of the automated routine"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "ID of the device receiving the command"
                        },
                        "device_status": {
                            "type": "string",
                            "description": "Status to set the device to (e.g., 'on', 'off')"
                        }
                    },
                    "required": ["device_type", "routine_id", "device_id", "device_status"]
                }
            }
        }
