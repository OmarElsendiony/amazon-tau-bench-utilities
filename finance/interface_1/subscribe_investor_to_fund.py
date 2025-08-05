import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubscribeInvestorToFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               amount: str, currency: str, request_assigned_to: str, 
               request_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate assigned user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"User {request_assigned_to} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "amount": amount,
            "currency": currency,
            "status": "pending",
            "request_assigned_to": request_assigned_to,
            "request_date": request_date,
            "approval_date": None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        return json.dumps(new_subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "subscribe_investor_to_fund",
                "description": "Subscribe an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "string", "description": "Subscription amount"},
                        "currency": {"type": "string", "description": "Currency of the subscription (USD, EUR, GBP, NGN)"},
                        "request_assigned_to": {"type": "string", "description": "ID of the user assigned to handle the request"},
                        "request_date": {"type": "string", "description": "Date of the subscription request in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "currency", "request_assigned_to", "request_date"]
                }
            }
        }
