import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        results = []
        
        for payment in payments.values():
            if invoice_id and payment.get("invoice_id") != invoice_id:
                continue
            if status and payment.get("status") != status:
                continue
            
            results.append(payment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payments",
                "description": "Get payments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "status": {"type": "string", "description": "Filter by payment status (draft, completed, failed)"}
                    },
                    "required": []
                }
            }
        }
