import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPaymentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        invoices = data.get("invoices", {})
        results = []
        
        # Get relevant invoice IDs based on filters
        relevant_invoice_ids = set()
        
        if invoice_id:
            relevant_invoice_ids.add(invoice_id)
        else:
            for invoice in invoices.values():
                if investor_id and invoice.get("investor_id") != investor_id:
                    continue
                if fund_id and invoice.get("fund_id") != fund_id:
                    continue
                relevant_invoice_ids.add(invoice.get("invoice_id"))
        
        # Filter payments by relevant invoices
        for payment in payments.values():
            if payment.get("invoice_id") in relevant_invoice_ids:
                results.append(payment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Get payment history with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": []
                }
            }
        }
