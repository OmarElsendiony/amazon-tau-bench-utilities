import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None, 
               fund_id: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_subscriptions",
                "description": "Retrieve subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Investor ID"},
                        "fund_id": {"type": "string", "description": "Fund ID"}
                    },
                    "required": []
                }
            }
        }
