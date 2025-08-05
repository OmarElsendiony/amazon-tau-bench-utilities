import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        if not filters:
            filters = {}
        
        for invoice in invoices.values():
            # Apply filters
            if filters.get("invoice_id") and invoice.get("invoice_id") != filters["invoice_id"]:
                continue
            if filters.get("fund_id") and invoice.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and invoice.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("commitment_id") and invoice.get("commitment_id") != filters["commitment_id"]:
                continue
            if filters.get("status") and invoice.get("status") != filters["status"]:
                continue
            if filters.get("currency") and invoice.get("currency") != filters["currency"]:
                continue
            if filters.get("payment_type") and invoice.get("payment_type") != filters["payment_type"]:
                continue
            
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoices",
                "description": "Get invoices based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (invoice_id, fund_id, investor_id, commitment_id, status, currency, payment_type)"
                        }
                    },
                    "required": []
                }
            }
        }
