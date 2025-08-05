import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, name: str, fund_type: str,
               base_currency: str, size: float, status: str) -> str:
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
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
        
        # Update fund details
        funds[str(fund_id)]["name"] = name
        funds[str(fund_id)]["fund_type"] = fund_type
        funds[str(fund_id)]["base_currency"] = base_currency
        funds[str(fund_id)]["size"] = size
        funds[str(fund_id)]["status"] = status
        funds[str(fund_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(funds[str(fund_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund_details",
                "description": "Update fund details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "size": {"type": "number", "description": "Fund size"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": ["fund_id", "name", "fund_type", "base_currency", "size", "status"]
                }
            }
        }
