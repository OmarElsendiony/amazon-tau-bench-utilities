import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDailyProfitLossByFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, date: str) -> str:
        nav_records = data.get("nav_records", {})
        trades = data.get("trades", {})
        
        # Find NAV records for the fund on the specified date and previous date
        current_nav = None
        previous_nav = None
        
        fund_navs = []
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id:
                fund_navs.append(nav)
        
        # Sort by date
        fund_navs.sort(key=lambda x: x.get("nav_date", ""))
        
        # Find current and previous NAV
        for i, nav in enumerate(fund_navs):
            if nav.get("nav_date") == date:
                current_nav = nav.get("nav_value", 0)
                if i > 0:
                    previous_nav = fund_navs[i-1].get("nav_value", 0)
                break
        
        if current_nav is None:
            raise ValueError(f"No NAV record found for fund {fund_id} on date {date}")
        
        # Calculate P&L
        if previous_nav is not None:
            pnl = float(current_nav) - float(previous_nav)
        else:
            pnl = 0.0  # First day, no previous data
        
        return json.dumps({"pnl": pnl})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_daily_profit_loss_by_fund",
                "description": "Get daily profit/loss for a fund on a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "date"]
                }
            }
        }
