import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AssignUserToHandleInvestorOrFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, investor_id: Optional[str] = None,
               fund_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User with ID {user_id} not found")
        
        if investor_id:
            # Validate investor exists
            if str(investor_id) not in investors:
                raise ValueError(f"Investor with ID {investor_id} not found")
            
            # Update investor's employee_id
            investors[str(investor_id)]["employee_id"] = str(user_id)
            return json.dumps(investors[str(investor_id)])
        
        elif fund_id:
            # Validate fund exists
            if str(fund_id) not in funds:
                raise ValueError(f"Fund with ID {fund_id} not found")
            
            # Update fund's manager_id
            funds[str(fund_id)]["manager_id"] = str(user_id)
            funds[str(fund_id)]["updated_at"] = "2025-10-01T00:00:00"
            return json.dumps(funds[str(fund_id)])
        
        else:
            raise ValueError("Either investor_id or fund_id must be provided")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_user_to_handle_investor_or_fund",
                "description": "Assign a user to handle an investor or fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to assign"},
                        "investor_id": {"type": "string", "description": "Investor ID (optional)"},
                        "fund_id": {"type": "string", "description": "Fund ID (optional)"}
                    },
                    "required": ["user_id"]
                }
            }
        }
