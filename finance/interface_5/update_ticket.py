import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: str,
               status: Optional[str] = None, resolution_date: Optional[str] = None,
               assigned_to: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        users = data.get("users", {})
        
        # Validate ticket exists
        if str(ticket_id) not in tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = tickets[str(ticket_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["open", "in_review", "resolved", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate assigned user if provided
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"User {assigned_to} not found")
        
        # Update fields
        if status:
            ticket["status"] = status
        if resolution_date:
            ticket["resolution_date"] = resolution_date
        if assigned_to:
            ticket["assigned_to"] = assigned_to
        
        ticket["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(ticket)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_ticket",
                "description": "Update an existing ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "ID of the ticket to update"},
                        "status": {"type": "string", "description": "New status (open, in_review, resolved, closed) (optional)"},
                        "resolution_date": {"type": "string", "description": "Resolution date (optional)"},
                        "assigned_to": {"type": "string", "description": "ID of the user to assign the ticket to (optional)"}
                    },
                    "required": ["ticket_id"]
                }
            }
        }
