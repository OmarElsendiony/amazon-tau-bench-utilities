import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, amount: str, 
               status: str) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "approved", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        timestamp = "2025-10-01T00:00:00"
        
        # Update subscription details
        subscription = subscriptions[str(subscription_id)]
        subscription["amount"] = amount
        subscription["status"] = status
        subscription["updated_at"] = timestamp
        
        # Set approval date if status is approved
        if status == "approved":
            subscription["approval_date"] = timestamp.split("T")[0]  # Extract date part
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update subscription amount and status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "amount": {"type": "string", "description": "New subscription amount"},
                        "status": {"type": "string", "description": "New subscription status (pending, approved, cancelled)"}
                    },
                    "required": ["subscription_id", "amount", "status"]
                }
            }
        }
