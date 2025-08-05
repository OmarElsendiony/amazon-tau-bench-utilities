import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_subscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None,
               currency: Optional[str] = None, request_assigned_to: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if status and subscription.get("status") != status:
                continue
            if currency and subscription.get("currency") != currency:
                continue
            if request_assigned_to and subscription.get("request_assigned_to") != request_assigned_to:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_subscriptions",
                "description": "Get subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, cancelled)"},
                        "currency": {"type": "string", "description": "Filter by currency (USD, EUR, GBP, NGN)"},
                        "request_assigned_to": {"type": "string", "description": "Filter by assigned user ID"}
                    },
                    "required": []
                }
            }
        }
