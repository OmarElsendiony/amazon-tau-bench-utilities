import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None,
               fund_id: Optional[str] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            if investor_id and invoice.get("investor_id") != investor_id:
                continue
            if fund_id and invoice.get("fund_id") != fund_id:
                continue
            if status and invoice.get("status") != status:
                continue
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoices",
                "description": "Retrieve invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"}
                    },
                    "required": []
                }
            }
        }
