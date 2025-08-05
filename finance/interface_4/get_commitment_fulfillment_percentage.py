import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from decimal import Decimal

class GetCommitmentFulfillmentPercentage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        commitment_amount = Decimal(str(commitment.get("commitment_amount", 0)))
        
        if commitment_amount == 0:
            return json.dumps({"fulfilled_percent": "0.00"})
        
        # Find all invoices for this commitment
        commitment_invoices = []
        for invoice in invoices.values():
            if invoice.get("commitment_id") == commitment_id:
                commitment_invoices.append(invoice)
        
        # Calculate total paid amount
        total_paid = Decimal("0")
        for invoice in commitment_invoices:
            invoice_id = invoice.get("invoice_id")
            for payment in payments.values():
                if (payment.get("invoice_id") == invoice_id and 
                    payment.get("status") == "completed"):
                    total_paid += Decimal(str(payment.get("amount", 0)))
        
        # Calculate percentage
        if commitment_amount > 0:
            percentage = (total_paid / commitment_amount) * 100
            percentage = min(percentage, Decimal("100"))  # Cap at 100%
        else:
            percentage = Decimal("0")
        
        return json.dumps({"fulfilled_percent": str(percentage.quantize(Decimal("0.01")))})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitment_fulfillment_percentage",
                "description": "Get the fulfillment percentage of a commitment based on completed payments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
