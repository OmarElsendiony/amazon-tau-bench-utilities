import json
from typing import Any, Dict, Optional
from datetime import datetime
import calendar
from tau_bench.envs.tool import Tool

class FetchHistoricalEnergyConsumptionByHome(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        home_id: str,
        date: Optional[str] = None,
        month: Optional[int] = None
    ) -> str:
        records = data.get("historical_energy_consumption", {})
        if not home_id:
            return json.dumps({"total_power_used_kWh": 0.0})

        filtered = [r for r in records.values() if str(r.get("home_id")) == home_id]

        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                year = dt.year
                month_num = dt.month
                day = dt.day
                target_day = 1 if day <= 14 else 15
                target_date = f"{year:04d}-{month_num:02d}-{target_day:02d}"

                total = sum(
                    r["power_used_kWh"]
                    for r in filtered
                    if r["date"] == target_date
                )
                return json.dumps({"total_power_used_kWh": round(total, 2)})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        elif month:
            try:
                year = 2025
                total_days = calendar.monthrange(year, month)[1]
                device_map = {}

                for r in filtered:
                    try:
                        r_date = datetime.strptime(r["date"], "%Y-%m-%d")
                        if r_date.month == month and r_date.year == year:
                            device_id = r["device_id"]
                            if device_id not in device_map:
                                device_map[device_id] = {}
                            if r_date.day == 1:
                                device_map[device_id]["first"] = r["power_used_kWh"]
                            elif r_date.day == 15:
                                device_map[device_id]["fifteenth"] = r["power_used_kWh"]
                    except Exception:
                        continue

                total_kWh = 0.0
                for device_data in device_map.values():
                    first_val = device_data.get("first")
                    fifteenth_val = device_data.get("fifteenth")

                    if first_val is not None and fifteenth_val is not None:
                        approx = first_val * 14 + fifteenth_val * (total_days - 14)
                    elif first_val is not None:
                        approx = first_val * total_days
                    elif fifteenth_val is not None:
                        approx = fifteenth_val * total_days
                    else:
                        approx = 0.0

                    total_kWh += approx

                return json.dumps({"total_power_used_kWh": round(total_kWh, 2)})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        return json.dumps({"total_power_used_kWh": 0.0})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_historical_energy_consumption_by_home",
                "description": "Returns estimated energy consumption for a home by date or month. Uses values from the 1st or 15th of the month for approximation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "home_id": {
                            "type": "string",
                            "description": "ID of the home to calculate energy consumption for"
                        },
                        "date": {
                            "type": "string",
                            "description": "Specific date in format YYYY-MM-DD. Uses either 1st or 15th to estimate daily usage."
                        },
                        "month": {
                            "type": "integer",
                            "description": "Month number (e.g. 5 for May). Uses weighted estimate between 1st and 15th of the month."
                        }
                    },
                    "required": ["home_id"]
                }
            }
        }
