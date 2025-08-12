import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommands(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: str = None,
               device_id: str = None) -> str:
        results = []
        
        # Define table configurations
        tables = [
            ("device_commands", "on_off_command", "device_command_id", {"status": "status"}),
            ("bulb_commands", "bulb_command", "bulb_command_id", {"brightness_level": "brightness_level", "color": "color"}),
            ("thermostat_commands", "thermostat_command", "thermostat_command_id", {"current_temperature": "current_temperature"})
        ]
        
        for table_name, command_type, id_field, specific_fields in tables:
            commands = data.get(table_name, {})
            
            for cmd in commands.values():
                # Apply filters based on the three cases
                if routine_id and device_id:
                    # Case 3: Both parameters given
                    if str(cmd.get("routine_id")) != routine_id or str(cmd.get("device_id")) != device_id:
                        continue
                elif routine_id:
                    # Case 1: Only routine_id given
                    if str(cmd.get("routine_id")) != routine_id:
                        continue
                elif device_id:
                    # Case 2: Only device_id given
                    if str(cmd.get("device_id")) != device_id:
                        continue
                else:
                    # Case 4: No parameters - skip all
                    continue
                
                # Build command info
                command_info = {
                    "command_type": command_type,
                    "command_id": cmd.get(id_field),
                    "routine_id": cmd.get("routine_id"),
                    "device_id": cmd.get("device_id"),
                    "created_at": cmd.get("created_at"),
                    "updated_at": cmd.get("updated_at")
                }
                
                # Add table-specific fields
                command_info.update({k: cmd.get(v) for k, v in specific_fields.items()})
                results.append(command_info)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commands",
                "description": "Retrieve commands from device_commands, bulb_commands, and thermostat_commands tables. Can filter by routine_id, device_id, or both. Returns all matching commands with their specific attributes.",
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