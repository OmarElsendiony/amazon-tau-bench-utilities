import json
from typing import Any, Dict, Optional
from datetime import datetime
import calendar
from tau_bench.envs.tool import Tool

class RetrieveHistoricalEnergyConsumptionByDevice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        device_id: Optional[str] = None,
        date: Optional[str] = None,
        month: Optional[int] = None
    ) -> str:
        records = data.get("historical_energy_consumption", {})

        if not device_id:
            return json.dumps({"total_power_used_kWh": 0.0})

        # Filter records by device_id (as string)
        filtered = [
            r for r in records.values()
            if str(r.get("device_id")) == device_id
        ]

        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                year = dt.year
                month = dt.month
                day = dt.day

                # Select either the 1st or 15th of the month
                target_day = 1 if day <= 14 else 15
                target_date = f"{year:04d}-{month:02d}-{target_day:02d}"

                match = next((r for r in filtered if r["date"] == target_date), None)
                return json.dumps({"total_power_used_kWh": match["power_used_kWh"] if match else 0.0})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        elif month:
            try:
                # Use current year (2025) for all calculations
                year = 2025
                total_days = calendar.monthrange(year, month)[1]
                first_val = None
                fifteenth_val = None

                for r in filtered:
                    try:
                        r_date = datetime.strptime(r["date"], "%Y-%m-%d")
                        if r_date.month == month and r_date.year == year:
                            if r_date.day == 1:
                                first_val = r["power_used_kWh"]
                            elif r_date.day == 15:
                                fifteenth_val = r["power_used_kWh"]
                    except Exception:
                        continue

                if first_val is not None and fifteenth_val is not None:
                    approx = first_val * 14 + fifteenth_val * (total_days - 14)
                elif first_val is not None:
                    approx = first_val * total_days
                elif fifteenth_val is not None:
                    approx = fifteenth_val * total_days
                else:
                    approx = 0.0

                return json.dumps({"total_power_used_kWh": round(approx, 2)})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        return json.dumps({"total_power_used_kWh": 0.0})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_historical_energy_consumption_by_device",
                "description": "Returns approximate power usage for a device. Uses the 1st or 15th of the month based on date, or weighted average for the full month.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {"type": "string", "description": "ID of the device (as string)"},
                        "date": {"type": "string", "description": "Format: YYYY-MM-DD"},
                        "month": {"type": "integer", "description": "Month as number, e.g., 5 for May"},
                    },
                    "required": ["device_id"]
                }
            }
        }
