import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, investor_id: Optional[str] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            # Apply filters
            if fund_id and str(invoice.get("fund_id")) != str(fund_id):
                continue
            if investor_id and str(invoice.get("investor_id")) != str(investor_id):
                continue
            if status and invoice.get("status") != status:
                continue
                
            results.append(invoice)
        
        # Sort by invoice date (newest first)
        results.sort(key=lambda x: x.get("invoice_date", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_invoices",
                "description": "Fetch invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"}
                    },
                    "required": []
                }
            }
        }
