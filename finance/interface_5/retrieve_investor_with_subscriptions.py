import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInvestorWithSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None,
               subscription_id: Optional[str] = None, name: Optional[str] = None,
               contact_email: Optional[str] = None, employee_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        
        # Find matching investors
        matching_investors = []
        for investor in investors.values():
            if investor_id and investor.get("investor_id") != investor_id:
                continue
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            if contact_email and investor.get("contact_email") != contact_email:
                continue
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            matching_investors.append(investor)
        
        # Add subscriptions to each matching investor
        results = []
        for investor in matching_investors:
            investor_with_subs = investor.copy()
            investor_subs = []
            
            for subscription in subscriptions.values():
                if subscription.get("investor_id") == investor.get("investor_id"):
                    if subscription_id and subscription.get("subscription_id") != subscription_id:
                        continue
                    investor_subs.append(subscription)
            
            investor_with_subs["subscriptions"] = investor_subs
            results.append(investor_with_subs)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_investor_with_subscriptions",
                "description": "Retrieve investors with their subscriptions using various filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "name": {"type": "string", "description": "Filter by investor name (partial match)"},
                        "contact_email": {"type": "string", "description": "Filter by contact email"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"}
                    },
                    "required": []
                }
            }
        }
