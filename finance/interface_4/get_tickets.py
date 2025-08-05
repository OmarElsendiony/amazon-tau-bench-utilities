import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTickets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        results = []
        
        for ticket in tickets.values():
            if invoice_id and ticket.get("invoice_id") != invoice_id:
                continue
            if status and ticket.get("status") != status:
                continue
            
            results.append(ticket)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_tickets",
                "description": "Get tickets with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "status": {"type": "string", "description": "Filter by ticket status (open, in_review, resolved, closed)"}
                    },
                    "required": []
                }
            }
        }
