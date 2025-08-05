import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, issue_date: str,
               type: str, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        tickets = data.get("tickets", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate type
        valid_types = ["missing_payment", "overpayment", "underpayment", 
                      "mismatched_amount", "invoice_duplicate", "manual_follow_up"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ["open", "in_review", "resolved", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        ticket_id = generate_id(tickets)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_ticket = {
            "ticket_id": str(ticket_id),
            "invoice_id": invoice_id,
            "issue_date": issue_date,
            "type": type,
            "status": status,
            "assigned_to": None,
            "resolution_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        tickets[str(ticket_id)] = new_ticket
        return json.dumps(new_ticket)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_ticket",
                "description": "Create a new ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "issue_date": {"type": "string", "description": "Issue date in ISO format"},
                        "type": {"type": "string", "description": "Ticket type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                        "status": {"type": "string", "description": "Ticket status (open, in_review, resolved, closed)"}
                    },
                    "required": ["invoice_id", "issue_date", "type", "status"]
                }
            }
        }
