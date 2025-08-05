import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePaymentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_id: str,
               amount: str, payment_method: str, status: str) -> str:
        payments = data.get("payments", {})
        
        if str(payment_id) not in payments:
            raise ValueError(f"Payment {payment_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        # Validate status
        valid_statuses = ["draft", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        payment = payments[str(payment_id)]
        payment["amount"] = amount
        payment["payment_method"] = payment_method
        payment["status"] = status
        
        return json.dumps(payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_payment_details",
                "description": "Update payment details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {"type": "string", "description": "ID of the payment"},
                        "amount": {"type": "string", "description": "Updated amount"},
                        "payment_method": {"type": "string", "description": "Updated payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Updated status (draft, completed, failed)"}
                    },
                    "required": ["payment_id", "amount", "payment_method", "status"]
                }
            }
        }
