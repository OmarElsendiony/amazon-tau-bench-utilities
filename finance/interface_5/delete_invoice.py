import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> str:
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        deleted_invoice = invoices[str(invoice_id)].copy()
        del invoices[str(invoice_id)]
        
        return json.dumps({"deleted_invoice": deleted_invoice, "status": "deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_invoice",
                "description": "Delete an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to delete"}
                    },
                    "required": ["invoice_id"]
                }
            }
        }
