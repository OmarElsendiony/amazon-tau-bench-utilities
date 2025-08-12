import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool


class IsExpiredWarrantyDevices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               current_date: str,
               device_id: Optional[str] = None,
               home_id: Optional[str] = None,
               room_id: Optional[str] = None) -> str:
        """
        Returns a list of devices with a boolean indicating whether their insurance/warranty has expired
        as of the given current_date. Filters can be applied by device_id, home_id, and room_id.
        """
        devices = data.get("devices", {})

        try:
            current_date_obj = datetime.strptime(str(current_date), "%Y-%m-%d").date()
        except Exception as e:
            return json.dumps({
                "error": f"Invalid current_date format. Expected YYYY-MM-DD. Error: {str(e)}"
            })

        result = []

        for device in devices.values():
            if device_id and str(device.get("device_id")) != device_id:
                continue
            if home_id and str(device.get("home_id")) != home_id:
                continue
            if room_id and str(device.get("room_id")) != room_id:
                continue

            insurance_str = device.get("insurance_expiry_date")
            try:
                insurance_date = datetime.strptime(insurance_str, "%Y-%m-%d").date()
                is_expired = insurance_date < current_date_obj
            except Exception:
                is_expired = True  # treat invalid date as expired

            result.append({
                "device_id": str(device.get("device_id")),
                "is_expired": is_expired
            })

        return json.dumps(result)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "is_expired_warrenty_devices",
                "description": "Check if device warranties (insurance_expiry_date) are expired as of current_date. Optional filters: device_id, home_id, room_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_date": {
                            "type": "string",
                            "description": "Current date in YYYY-MM-DD format"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Filter by specific device ID"
                        },
                        "home_id": {
                            "type": "string",
                            "description": "Filter by home ID"
                        },
                        "room_id": {
                            "type": "string",
                            "description": "Filter by room ID"
                        }
                    },
                    "required": ["current_date"]
                }
            }
        }
