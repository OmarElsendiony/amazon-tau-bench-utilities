import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorWithSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: Optional[str] = None,
               name: Optional[str] = None, contact_email: Optional[str] = None,
               employee_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for investor in investors.values():
            # Apply filters
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            if contact_email and investor.get("contact_email", "").lower() != contact_email.lower():
                continue
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            
            # Get investor's subscriptions
            investor_subscriptions = []
            for subscription in subscriptions.values():
                if subscription.get("investor_id") == investor.get("investor_id"):
                    if subscription_id and subscription.get("subscription_id") != subscription_id:
                        continue
                    investor_subscriptions.append(subscription)
            
            # If subscription_id filter is applied and no matching subscription found, skip
            if subscription_id and not investor_subscriptions:
                continue
            
            investor_with_subs = investor.copy()
            investor_with_subs["subscriptions"] = investor_subscriptions
            results.append(investor_with_subs)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_with_subscriptions",
                "description": "Get investors with their subscriptions based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "name": {"type": "string", "description": "Filter by investor name"},
                        "contact_email": {"type": "string", "description": "Filter by contact email"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"}
                    },
                    "required": []
                }
            }
        }
