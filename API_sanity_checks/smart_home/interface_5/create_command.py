import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommand(Tool):
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
        command_id = generate_id(device_commands)
        device_commands[command_id] = {
            "device_command_id": command_id,
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
                "name": "create_command",
                "description": "Creates a command for any device type and stores it in the device_commands table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {
                            "type": "string",
                            "description": "Type of device receiving the command"
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "ID of the routine issuing the command"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Target device ID"
                        },
                        "device_status": {
                            "type": "string",
                            "description": "Status to apply to the device (e.g., 'on', 'off')"
                        }
                    },
                    "required": ["device_type", "routine_id", "device_id", "device_status"]
                }
            }
        }
