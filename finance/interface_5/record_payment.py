import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_date: str,
               amount: str, payment_method: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        payments = data.get("payments", {})
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate payment_method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment_method. Must be one of {valid_methods}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_payment = {
            "payment_id": str(payment_id),
            "invoice_id": invoice_id,
            "payment_date": payment_date,
            "amount": amount,
            "payment_method": payment_method,
            "status": "completed",
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        return json.dumps(new_payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_payment",
                "description": "Record a new payment for an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Payment date"},
                        "amount": {"type": "string", "description": "Payment amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"}
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }
