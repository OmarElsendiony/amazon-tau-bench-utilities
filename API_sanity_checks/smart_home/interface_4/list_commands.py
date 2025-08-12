import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListCommands(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: str = None,
               device_id: str = None) -> str:
        results = []
        
        tables = [
            ("device_commands", "on_off_command", "device_command_id", {"status": "status"}),
            ("bulb_commands", "bulb_command", "bulb_command_id", {"brightness_level": "brightness_level", "color": "color"}),
            ("thermostat_commands", "thermostat_command", "thermostat_command_id", {"current_temperature": "current_temperature"})
        ]
        
        for table_name, command_type, id_field, specific_fields in tables:
            commands = data.get(table_name, {})
            
            for cmd in commands.values():
                if routine_id and device_id:
                    if str(cmd.get("routine_id")) != routine_id or str(cmd.get("device_id")) != device_id:
                        continue
                elif routine_id:
                    if str(cmd.get("routine_id")) != routine_id:
                        continue
                elif device_id:
                    if str(cmd.get("device_id")) != device_id:
                        continue
                else:
                    continue
                
                command_info = {
                    "command_type": command_type,
                    "command_id": cmd.get(id_field),
                    "routine_id": cmd.get("routine_id"),
                    "device_id": cmd.get("device_id"),
                    "created_at": cmd.get("created_at"),
                    "updated_at": cmd.get("updated_at")
                }
                
                command_info.update({k: cmd.get(v) for k, v in specific_fields.items()})
                results.append(command_info)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_commands",
                "description": "List all commands from device_commands, bulb_commands, and thermostat_commands. Filters supported: routine_id, device_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {"type": "string", "description": "Filter commands by routine ID"},
                        "device_id": {"type": "string", "description": "Filter commands by device ID"}
                    },
                    "required": []
                }
            }
        }
