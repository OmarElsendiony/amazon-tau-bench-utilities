import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifySubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str,
               amount: Optional[str] = None, currency: Optional[str] = None,
               status: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        subscription = subscriptions[str(subscription_id)]
        
        # Validate currency if provided
        if currency:
            valid_currencies = ["USD", "EUR", "GBP", "NGN"]
            if currency not in valid_currencies:
                raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        # Validate status if provided
        if status:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if amount:
            subscription["amount"] = amount
        if currency:
            subscription["currency"] = currency
        if status:
            subscription["status"] = status
            if status == "approved":
                subscription["approval_date"] = "2025-10-01"
        
        subscription["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_subscription",
                "description": "Modify an existing subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to modify"},
                        "amount": {"type": "string", "description": "New subscription amount (optional)"},
                        "currency": {"type": "string", "description": "New currency (USD, EUR, GBP, NGN) (optional)"},
                        "status": {"type": "string", "description": "New status (pending, approved, cancelled) (optional)"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
