import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_commitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None,
               currency: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if status and commitment.get("status") != status:
                continue
            if currency and commitment.get("currency") != currency:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"},
                        "currency": {"type": "string", "description": "Filter by currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": []
                }
            }
        }
