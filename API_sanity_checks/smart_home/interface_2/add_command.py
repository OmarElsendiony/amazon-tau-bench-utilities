import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddCommand(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               routine_id: str,
               device_id: str,
               device_status: str,
               thermostat_new_current_temperature: float = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00"

        # Add to device_commands
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

        # If it's a thermostat and temperature is provided, add to thermostat_commands
        if device_type == "thermostat" and thermostat_new_current_temperature is not None:
            thermostat_commands = data.setdefault("thermostat_commands", {})
            tcid = generate_id(thermostat_commands)
            thermostat_commands[tcid] = {
                "thermostat_command_id": tcid,
                "routine_id": routine_id,
                "device_id": device_id,
                "current_temperature": thermostat_new_current_temperature,
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
                "description": "Add a command to a routine. If the device is a thermostat and temperature is provided, also adds a thermostat command.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {
                            "type": "string",
                            "description": "Type of the device (e.g., 'thermostat')"
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "ID of the routine"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "ID of the device"
                        },
                        "device_status": {
                            "type": "string",
                            "description": "Status to set the device to (e.g., 'on', 'off')"
                        },
                        "thermostat_new_current_temperature": {
                            "type": "number",
                            "description": "New temperature to set (for thermostat only)"
                        }
                    },
                    "required": ["device_type", "routine_id", "device_id", "device_status"]
                }
            }
        }
