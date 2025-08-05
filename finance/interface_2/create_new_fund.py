import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, fund_type: str, base_currency: str,
               manager_id: str, size: float, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(manager_id) not in users:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate fund_type
        valid_fund_types = ["equity", "fixed_income", "multi_asset", "hedge"]
        if fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
        
        # Validate base_currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid base currency. Must be one of {valid_currencies}")
        
        # Validate status
        valid_statuses = ["open", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00"
        
        new_fund = {
            "fund_id": str(fund_id),
            "name": name,
            "fund_type": fund_type,
            "base_currency": base_currency,
            "manager_id": str(manager_id),
            "size": size,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[str(fund_id)] = new_fund
        return json.dumps(new_fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_fund",
                "description": "Create a new fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "manager_id": {"type": "string", "description": "Manager user ID"},
                        "size": {"type": "number", "description": "Fund size"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": ["name", "fund_type", "base_currency", "manager_id", "size", "status"]
                }
            }
        }
