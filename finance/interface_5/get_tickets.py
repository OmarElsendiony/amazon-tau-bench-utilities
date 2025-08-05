import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTickets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: Optional[str] = None,
               invoice_id: Optional[str] = None, type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        results = []
        
        for ticket in tickets.values():
            if ticket_id and ticket.get("ticket_id") != ticket_id:
                continue
            if invoice_id and ticket.get("invoice_id") != invoice_id:
                continue
            if type and ticket.get("type") != type:
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
                        "ticket_id": {"type": "string", "description": "Filter by ticket ID"},
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "type": {"type": "string", "description": "Filter by type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                        "status": {"type": "string", "description": "Filter by status (open, in_review, resolved, closed)"}
                    },
                    "required": []
                }
            }
        }
