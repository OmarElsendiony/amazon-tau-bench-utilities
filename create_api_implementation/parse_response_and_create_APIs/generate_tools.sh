#!/usr/bin/env bash
set -e

# Tool: acknowledge_or_resolve_alert
cat > acknowledge_or_resolve_alert.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class acknowledge_or_resolve_alert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               alert_id: str,
               acknowledged_at: Optional[str] = None,
               acknowledged_by_user: Optional[str] = None,
               resolved_at: Optional[str] = None,
               resolved_by_user: Optional[str] = None) -> str:

        alerts = data.get("emergency_alerts", {})

        # Fetch and validate alert
        alert = alerts.get(alert_id)
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        # Update fields if provided
        if acknowledged_at is not None:
            alert["acknowledged_at"] = acknowledged_at
        if acknowledged_by_user is not None:
            alert["acknowledged_by_user"] = acknowledged_by_user
        if resolved_at is not None:
            alert["resolved_at"] = resolved_at
        if resolved_by_user is not None:
            alert["resolved_by_user"] = resolved_by_user

        # Stamp update time
        alert["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(alert)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "acknowledge_or_resolve_alert",
                "description": "Acknowledges or resolves an emergency alert by updating its timestamps and users",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alert_id": {"type": "string", "description": "ID of the alert"},
                        "acknowledged_at": {"type": "string", "description": "Timestamp of acknowledgment"},
                        "acknowledged_by_user": {"type": "string", "description": "User ID who acknowledged"},
                        "resolved_at": {"type": "string", "description": "Timestamp of resolution"},
                        "resolved_by_user": {"type": "string", "description": "User ID who resolved"}
                    },
                    "required": ["alert_id"]
                }
            }
        }
EOF

# Tool: add_command
cat > add_command.py << 'EOF'
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
EOF

# Tool: add_feedback
cat > add_feedback.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class add_feedback(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               device_id: str,
               rating: int) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        feedbacks = data.get("user_feedbacks", {})
        fb_id = generate_id(feedbacks)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_fb = {
            "user_feedback_id": fb_id,
            "user_id": user_id,
            "device_id": device_id,
            "rating": rating,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        feedbacks[fb_id] = new_fb
        return json.dumps({"user_feedback_id": fb_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_feedback",
                "description": "Adds user feedback (rating) for a device",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "rating": {"type": "integer", "description": "Rating value"}
                    },
                    "required": ["user_id", "device_id", "rating"]
                }
            }
        }
EOF

# Tool: create_address
cat > create_address.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_address(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               house_number: str,
               building_name: str,
               street: str,
               city_name: str,
               state: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        addresses = data.get("addresses", {})
        addr_id = generate_id(addresses)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_addr = {
            "address_id": addr_id,
            "house_number": house_number,
            "building_name": building_name,
            "street": street,
            "city_name": city_name,
            "state": state,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        addresses[addr_id] = new_addr
        return json.dumps({"address_id": addr_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_address",
                "description": "Creates a new address entry in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "house_number": {"type": "string", "description": "House or unit number"},
                        "building_name": {"type": "string", "description": "Building name"},
                        "street": {"type": "string", "description": "Street name"},
                        "city_name": {"type": "string", "description": "City name"},
                        "state": {"type": "string", "description": "State name"}
                    },
                    "required": ["house_number", "building_name", "street", "city_name", "state"]
                }
            }
        }
EOF

# Tool: create_emergency_alert
cat > create_emergency_alert.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_emergency_alert(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               device_id: str,
               alert_type: str,
               severity_level: str,
               triggered_at: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        alerts = data.get("emergency_alerts", {})
        alert_id = generate_id(alerts)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_alert = {
            "alert_id": alert_id,
            "home_id": home_id,
            "device_id": device_id,
            "alert_type": alert_type,
            "severity_level": severity_level,
            "triggered_at": triggered_at,
            "acknowledged_at": None,
            "acknowledged_by_user": None,
            "resolved_at": None,
            "resolved_by_user": None,
            "created_at": timestamp
        }
        alerts[alert_id] = new_alert
        return json.dumps({"alert_id": alert_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_emergency_alert",
                "description": "Creates a new emergency alert for a device in a home",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "ID of the home"},
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "alert_type": {"type": "string", "description": "Type of alert"},
                        "severity_level": {"type": "string", "description": "Severity level (low, medium, high, critical)"},
                        "triggered_at": {"type": "string", "description": "Timestamp when alert was triggered"}
                    },
                    "required": ["home_id", "device_id", "alert_type", "severity_level", "triggered_at"]
                }
            }
        }
EOF

# Tool: get_address
cat > get_address.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_address(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               address_id: Optional[str] = None,
               house_number: Optional[str] = None,
               building_name: Optional[str] = None,
               street: Optional[str] = None,
               city_name: Optional[str] = None,
               state: Optional[str] = None) -> str:

        addresses = data.get("addresses", {})
        results = []

        for addr in addresses.values():
            if address_id and addr.get("address_id") != address_id:
                continue
            if house_number and addr.get("house_number", "").lower() != house_number.lower():
                continue
            if building_name and addr.get("building_name", "").lower() != building_name.lower():
                continue
            if street and addr.get("street", "").lower() != street.lower():
                continue
            if city_name and addr.get("city_name", "").lower() != city_name.lower():
                continue
            if state and addr.get("state", "").lower() != state.lower():
                continue
            results.append(addr)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_address",
                "description": "Retrieves address records matching the provided fields",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address_id": {"type": "string", "description": "Filter by address ID"},
                        "house_number": {"type": "string", "description": "Filter by house number"},
                        "building_name": {"type": "string", "description": "Filter by building name"},
                        "street": {"type": "string", "description": "Filter by street"},
                        "city_name": {"type": "string", "description": "Filter by city"},
                        "state": {"type": "string", "description": "Filter by state"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: get_commands
cat > get_commands.py << 'EOF'
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
EOF

# Tool: create_routine
cat > create_routine.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_routine(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               home_id: str,
               action_time: str,
               start_action_date: str,
               action_interval: str) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        routines = data.get("automated_routines", {})
        routine_id = generate_id(routines)
        timestamp = "2025-10-01T00:00:00ZZ"
        new_routine = {
            "routine_id": routine_id,
            "user_id": user_id,
            "home_id": home_id,
            "action_time": action_time,
            "start_action_date": start_action_date,
            "action_interval": action_interval,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        routines[routine_id] = new_routine
        return json.dumps({"routine_id": routine_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_routine",
                "description": "Creates a new automated routine for a user at a specific home",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"},
                        "home_id": {"type": "string", "description": "Home ID"},
                        "action_time": {"type": "string", "description": "Time to perform action (HH:MM:SS)"},
                        "start_action_date": {"type": "string", "description": "Date to start actions (YYYY-MM-DD)"},
                        "action_interval": {"type": "string", "description": "Interval (daily, one_time, every_hour)"}
                    },
                    "required": ["user_id", "home_id", "action_time", "start_action_date", "action_interval"]
                }
            }
        }
EOF

# Tool: get_emergency_alerts
cat > get_emergency_alerts.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_emergency_alerts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               device_id: Optional[str] = None,
               alert_type: Optional[str] = None,
               severity_level: Optional[str] = None,
               acknowledged_by_user: Optional[str] = None,
               resolved_by_user: Optional[str] = None) -> str:

        results = []
        for alert in data.get("emergency_alerts", {}).values():
            if home_id and alert.get("home_id") != home_id:
                continue
            if device_id and alert.get("device_id") != device_id:
                continue
            if alert_type and alert.get("alert_type") != alert_type:
                continue
            if severity_level and alert.get("severity_level") != severity_level:
                continue
            if acknowledged_by_user and str(alert.get("acknowledged_by_user")) != acknowledged_by_user:
                continue
            if resolved_by_user and str(alert.get("resolved_by_user")) != resolved_by_user:
                continue
            results.append(alert)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_emergency_alerts",
                "description": "Returns alerts filtered by home, device, alert type, severity, or user IDs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "device_id": {"type": "string", "description": "Filter by device ID"},
                        "alert_type": {"type": "string", "description": "Filter by alert type"},
                        "severity_level": {"type": "string", "description": "Filter by severity level"},
                        "acknowledged_by_user": {"type": "string", "description": "Filter by acknowledging user ID"},
                        "resolved_by_user": {"type": "string", "description": "Filter by resolving user ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: get_historical_energy_consumption_by_device
cat > get_historical_energy_consumption_by_device.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_historical_energy_consumption_by_device(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               date: Optional[str] = None,
               month: Optional[int] = None) -> str:

        total = 0.0
        for rec in data.get("historical_energy_consumption", {}).values():
            if rec.get("device_id") != device_id:
                continue
            rec_date = rec.get("date", "")
            if date and rec_date != date:
                continue
            if month:
                parts = rec_date.split("-")
                if len(parts) >= 2 and int(parts[1]) != month:
                    continue
            total += float(rec.get("power_used_kWh", 0))

        return json.dumps({"total_power_used_kWh": total})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_historical_energy_consumption_by_device",
                "description": "Returns device’s estimated energy usage using filters by date or month",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "date": {"type": "string", "description": "Filter by exact date (YYYY-MM-DD)"},
                        "month": {"type": "integer", "description": "Filter by month (1-12)"}
                    },
                    "required": ["device_id"]
                }
            }
        }
EOF

# Tool: update_device_info
cat > update_device_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_device_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_id: str,
               room_id: Optional[str] = None,
               installed_on: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               width_ft: Optional[float] = None,
               length_ft: Optional[float] = None,
               price: Optional[float] = None,
               scheduled_maintainance_date: Optional[str] = None,
               last_maintainance_date: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None,
               brightness_level: Optional[str] = None,
               color: Optional[str] = None) -> str:

        devices = data.get("devices", {})
        device = devices.get(device_id)
        if not device:
            raise ValueError(f"Device {device_id} not found")

        # Update main device fields
        for field, val in [
            ("room_id", room_id),
            ("installed_on", installed_on),
            ("insurance_expiry_date", insurance_expiry_date),
            ("home_id", home_id),
            ("status", status),
            ("width_ft", width_ft),
            ("length_ft", length_ft),
            ("price", price),
            ("scheduled_maintainance_date", scheduled_maintainance_date),
            ("last_maintainance_date", last_maintainance_date),
            ("daily_rated_power_consumption_kWh", daily_rated_power_consumption_kWh)
        ]:
            if val is not None:
                device[field] = val

        # Stamp update
        device["updated_at"] = "2025-10-01T00:00:00ZZ"

        # If bulb, update smart_bulbs record
        bulbs = data.get("smart_bulbs", {})
        if device_id in bulbs:
            bulb = bulbs[device_id]
            if brightness_level is not None:
                bulb["brightness_level"] = brightness_level
            if color is not None:
                bulb["color"] = color
            bulb["updated_at"] = "2025-10-01T00:00:00ZZ"

        return json.dumps(device)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_device_info",
                "description": "Updates a device’s attributes; also updates smart bulb info if applicable",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device"},
                        "room_id": {"type": "string", "description": "New room ID"},
                        "installed_on": {"type": "string", "description": "New install date"},
                        "insurance_expiry_date": {"type": "string", "description": "New insurance expiry date"},
                        "home_id": {"type": "string", "description": "New home ID"},
                        "status": {"type": "string", "description": "New status (on/off)"},
                        "width_ft": {"type": "number", "description": "New width in feet"},
                        "length_ft": {"type": "number", "description": "New length in feet"},
                        "price": {"type": "number", "description": "New price"},
                        "scheduled_maintainance_date": {"type": "string", "description": "New scheduled maintenance date"},
                        "last_maintainance_date": {"type": "string", "description": "New last maintenance date"},
                        "daily_rated_power_consumption_kWh": {"type": "number", "description": "New daily power consumption"},
                        "brightness_level": {"type": "string", "description": "New brightness level for bulb"},
                        "color": {"type": "string", "description": "New color for bulb"}
                    },
                    "required": ["device_id"]
                }
            }
        }
EOF

# Tool: update_room_info
cat > update_room_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_room_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: Optional[str] = None,
               status: Optional[str] = None) -> str:

        rooms = data.get("rooms", {})
        room = rooms.get(room_id)
        if not room:
            raise ValueError(f"Room {room_id} not found")

        # Assign owner and auto-occupy
        if room_owner_id is not None:
            room["room_owner_id"] = room_owner_id
            room["status"] = "occupied"

        # Update status if provided
        if status is not None:
            room["status"] = status

        room["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(room)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_room_info",
                "description": "Updates room owner or status; assigning owner auto-occupies room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string", "description": "ID of the room"},
                        "room_owner_id": {"type": "string", "description": "New owner user ID"},
                        "status": {"type": "string", "description": "New status (vacant, occupied)"}
                    },
                    "required": ["room_id"]
                }
            }
        }
EOF

# Tool: update_user_info
cat > update_user_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_user_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None,
               phone_number: Optional[str] = None,
               role: Optional[str] = None,
               email: Optional[str] = None,
               primary_address_id: Optional[str] = None) -> str:

        users = data.get("users", {})
        user = users.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        for field, val in [
            ("first_name", first_name),
            ("last_name", last_name),
            ("phone_number", phone_number),
            ("role", role),
            ("email", email),
            ("primary_address_id", primary_address_id)
        ]:
            if val is not None:
                user[field] = val

        user["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_info",
                "description": "Updates user record fields by user_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "first_name": {"type": "string", "description": "New first name"},
                        "last_name": {"type": "string", "description": "New last name"},
                        "phone_number": {"type": "string", "description": "New phone number"},
                        "role": {"type": "string", "description": "New role"},
                        "email": {"type": "string", "description": "New email"},
                        "primary_address_id": {"type": "string", "description": "New primary address ID"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# Tool: add_device
cat > add_device.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class add_device(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               device_type: str,
               room_id: str,
               home_id: str,
               width_ft: float,
               length_ft: float,
               price: float,
               daily_rated_power_consumption_kWh: float,
               brightness_level: Optional[str] = None,
               color: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None) -> str:

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        devices = data.get("devices", {})
        device_id = generate_id(devices)
        timestamp = "2025-10-01T00:00:00ZZ"

        new_device = {
            "device_id": device_id,
            "device_type": device_type,
            "room_id": room_id,
            "home_id": home_id,
            "installed_on": timestamp,
            "insurance_expiry_date": insurance_expiry_date,
            "status": "off",
            "width_ft": width_ft,
            "length_ft": length_ft,
            "price": price,
            "scheduled_maintainance_date": None,
            "last_maintainance_date": None,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        devices[device_id] = new_device

        # If bulb, also create smart_bulb entry
        if device_type == "bulb":
            bulbs = data.get("smart_bulbs", {})
            bulbs[device_id] = {
                "device_id": device_id,
                "brightness_level": brightness_level,
                "color": color,
                "created_at": timestamp,
                "updated_at": timestamp
            }

        return json.dumps({"device_id": device_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_device",
                "description": "Adds a new device; if a bulb, also creates smart bulb entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_type": {"type": "string", "description": "Type of device"},
                        "room_id": {"type": "string", "description": "Room ID"},
                        "home_id": {"type": "string", "description": "Home ID"},
                        "width_ft": {"type": "number", "description": "Width in feet"},
                        "length_ft": {"type": "number", "description": "Length in feet"},
                        "price": {"type": "number", "description": "Price"},
                        "daily_rated_power_consumption_kWh": {
                            "type": "number",
                            "description": "Daily power consumption"
                        },
                        "brightness_level": {
                            "type": "string",
                            "description": "Initial brightness (for bulb)"
                        },
                        "color": {"type": "string", "description": "Initial color (for bulb)"},
                        "insurance_expiry_date": {
                            "type": "string",
                            "description": "Insurance expiry date"
                        }
                    },
                    "required": [
                        "device_type",
                        "room_id",
                        "home_id",
                        "width_ft",
                        "length_ft",
                        "price",
                        "daily_rated_power_consumption_kWh"
                    ]
                }
            }
        }
EOF

# Tool: get_devices_info
cat > get_devices_info.py << 'EOF'
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
EOF

# Tool: get_energy_tariffs_info
cat > get_energy_tariffs_info.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_energy_tariffs_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str) -> str:

        results = []
        for t in data.get("energy_tariffs", {}).values():
            if t.get("home_id") == home_id:
                results.append(t)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_energy_tariffs_info",
                "description": "Fetches all energy tariff records for the given home ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Home ID"}
                    },
                    "required": ["home_id"]
                }
            }
        }
EOF

# Tool: get_home_info
cat > get_home_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_home_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: Optional[str] = None,
               owner_id: Optional[str] = None,
               address_id: Optional[str] = None) -> str:

        results = []
        homes = data.get("homes", {})
        rooms = data.get("rooms", {})

        for h in homes.values():
            if home_id and h.get("home_id") != home_id:
                continue
            if owner_id and h.get("owner_id") != owner_id:
                continue
            if address_id and h.get("address_id") != address_id:
                continue

            # Compute stats
            residents = {
                room.get("room_owner_id")
                for room in rooms.values()
                if room.get("home_id") == h.get("home_id") and room.get("room_owner_id")
            }
            occupied = sum(
                1 for room in rooms.values()
                if room.get("home_id") == h.get("home_id") and room.get("status") == "occupied"
            )

            rec = h.copy()
            rec["num_residents"] = len(residents)
            rec["num_rooms_occupied"] = occupied
            results.append(rec)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_home_info",
                "description": "Retrieves home info with resident and room occupancy stats",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "owner_id": {"type": "string", "description": "Filter by owner ID"},
                        "address_id": {"type": "string", "description": "Filter by address ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: get_rooms_info
cat > get_rooms_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_rooms_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               room_id: Optional[str] = None,
               home_id: Optional[str] = None) -> str:

        results = []
        for r in data.get("rooms", {}).values():
            if room_id and r.get("room_id") != room_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue
            results.append(r)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_rooms_info",
                "description": "Fetches room records filtered by room_id or home_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {"type": "string", "description": "Filter by room ID"},
                        "home_id": {"type": "string", "description": "Filter by home ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: get_routines
cat > get_routines.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_routines(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               routine_id: Optional[str] = None,
               user_id: Optional[str] = None,
               home_id: Optional[str] = None,
               action_time: Optional[str] = None,
               action_interval: Optional[str] = None,
               start_action_date: Optional[str] = None) -> str:

        results = []
        for r in data.get("automated_routines", {}).values():
            if routine_id and r.get("routine_id") != routine_id:
                continue
            if user_id and r.get("user_id") != user_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue
            if action_time and r.get("action_time") != action_time:
                continue
            if action_interval and r.get("action_interval") != action_interval:
                continue
            if start_action_date and r.get("start_action_date") != start_action_date:
                continue
            results.append(r)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_routines",
                "description": "Retrieves automated routines based on various optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "routine_id": {"type": "string", "description": "Filter by routine ID"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "home_id": {"type": "string", "description": "Filter by home ID"},
                        "action_time": {"type": "string", "description": "Filter by action time"},
                        "action_interval": {"type": "string", "description": "Filter by interval"},
                        "start_action_date": {"type": "string", "description": "Filter by start date"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: get_user_info
cat > get_user_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: Optional[str] = None,
               phone_number: Optional[str] = None,
               email: Optional[str] = None) -> str:

        results = []
        for u in data.get("users", {}).values():
            if user_id and u.get("user_id") != user_id:
                continue
            if phone_number and not u.get("phone_number", "").endswith(phone_number):
                continue
            if email and not u.get("email", "").lower().endswith(email.lower()):
                continue
            results.append(u)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Retrieves user records by user_id, phone, or email with case-insensitive/suffix matching",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "phone_number": {"type": "string", "description": "Filter by end of phone number"},
                        "email": {"type": "string", "description": "Filter by end of email address"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool: update_home_info
cat > update_home_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_home_info(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: Optional[str] = None,
               address_id: Optional[str] = None,
               home_type: Optional[str] = None) -> str:

        homes = data.get("homes", {})
        home = homes.get(home_id)
        if not home:
            raise ValueError(f"Home {home_id} not found")

        if owner_id is not None:
            home["owner_id"] = owner_id
        if address_id is not None:
            home["address_id"] = address_id
        if home_type is not None:
            home["home_type"] = home_type

        home["updated_at"] = "2025-10-01T00:00:00ZZ"
        return json.dumps(home)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_home_info",
                "description": "Updates a home’s owner, address, or type if provided",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {"type": "string", "description": "ID of the home"},
                        "owner_id": {"type": "string", "description": "New owner user ID"},
                        "address_id": {"type": "string", "description": "New address ID"},
                        "home_type": {"type": "string", "description": "New home type (Home, Apartment)"}
                    },
                    "required": ["home_id"]
                }
            }
        }
EOF

# Tool: list_children
cat > list_children.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class list_children(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               parent_id: str) -> str:

        results = [
            u for u in data.get("users", {}).values()
            if u.get("parent_id") == parent_id
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_children",
                "description": "Lists all users whose parent_id matches the given one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string", "description": "User ID of the parent"}
                    },
                    "required": ["parent_id"]
                }
            }
        }
EOF

echo "All tool files have been generated."
