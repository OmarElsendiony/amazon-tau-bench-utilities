import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        notifications = data.get("notifications", {})
        results = []
        
        for notification in notifications.values():
            match = True
            
            for key, value in filters.items():
                if key in notification and notification[key] != value:
                    match = False
                    break
            
            if match:
                results.append(notification)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_notifications",
                "description": "Retrieve notifications with filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Dictionary of filters to apply (email, type, class, reference_id, status)",
                            "properties": {
                                "email": {"type": "string", "description": "Filter by email"},
                                "type": {"type": "string", "description": "Filter by type (alert, report, reminder, subscription_update)"},
                                "class": {"type": "string", "description": "Filter by class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                                "reference_id": {"type": "string", "description": "Filter by reference ID"},
                                "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"}
                            }
                        }
                    },
                    "required": ["filters"]
                }
            }
        }
