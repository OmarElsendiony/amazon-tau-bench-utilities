import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str,
               amount: str, due_date: str, status: str) -> str:
        invoices = data.get("invoices", {})
        
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate status
        valid_statuses = ["issued", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        invoice = invoices[str(invoice_id)]
        invoice["amount"] = amount
        invoice["due_date"] = due_date
        invoice["status"] = status
        invoice["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice",
                "description": "Update invoice details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "amount": {"type": "string", "description": "Updated amount"},
                        "due_date": {"type": "string", "description": "Updated due date in YYYY-MM-DD format"},
                        "status": {"type": "string", "description": "Updated status (issued, paid)"}
                    },
                    "required": ["invoice_id", "amount", "due_date", "status"]
                }
            }
        }
