import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class IssueInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_id: str, invoice_date: str, due_date: str,
               amount: str, currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_invoice = {
            "invoice_id": str(invoice_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": amount,
            "payment_type": "manual",
            "currency": currency,
            "status": "issued",
            "updated_at": timestamp
        }
        
        invoices[str(invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "issue_invoice",
                "description": "Issue a new invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "amount": {"type": "string", "description": "Invoice amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_id", "invoice_date", "due_date", "amount", "currency"]
                }
            }
        }
