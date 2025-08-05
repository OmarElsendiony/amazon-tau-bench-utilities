import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_commands(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: Optional[str] = None,
               device_id: Optional[str] = None) -> str:

        results = []

        # Generic device commands
        for cmd in data.get("device_commands", {}).values():
            if routine_id and cmd.get("routine_id") != routine_id:
                continue
            if device_id and cmd.get("device_id") != device_id:
                continue
            results.append({
                "command_type": "device_command",
                "command_id": cmd.get("device_command_id"),
                "routine_id": cmd.get("routine_id"),
                "device_id": cmd.get("device_id"),
                "status": cmd.get("status"),
                "created_at": cmd.get("created_at"),
                "updated_at": cmd.get("updated_at")
            })

        # Bulb-specific commands
        for cmd in data.get("bulb_commands", {}).values():
            if routine_id and cmd.get("routine_id") != routine_id:
                continue
            if device_id and cmd.get("device_id") != device_id:
                continue
            results.append({
                "command_type": "bulb_command",
                "command_id": cmd.get("bulb_command_id"),
                "routine_id": cmd.get("routine_id"),
                "device_id": cmd.get("device_id"),
                "brightness_level": cmd.get("brightness_level"),
                "color": cmd.get("color"),
                "created_at": cmd.get("created_at"),
                "updated_at": cmd.get("updated_at")
            })

        # Thermostat-specific commands
        for cmd in data.get("thermostat_commands", {}).values():
            if routine_id and cmd.get("routine_id") != routine_id:
                continue
            if device_id and cmd.get("device_id") != device_id:
                continue
            results.append({
                "command_type": "thermostat_command",
                "command_id": cmd.get("thermostat_command_id"),
                "routine_id": cmd.get("routine_id"),
                "device_id": cmd.get("device_id"),
                "current_temperature": cmd.get("current_temperature"),
                "created_at": cmd.get("created_at"),
                "updated_at": cmd.get("updated_at")
            })

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commands",
                "description": "Retrieves commands from various tables based on routine/device filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {"type": "string", "description": "Filter by routine ID"},
                        "device_id": {"type": "string", "description": "Filter by device ID"}
                    },
                    "required": []
                }
            }
        }
