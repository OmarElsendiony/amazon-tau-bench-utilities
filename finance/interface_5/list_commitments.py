import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None,
               amount: Optional[str] = None, commitment_date: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if commitment_id and commitment.get("commitment_id") != commitment_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if amount and str(commitment.get("commitment_amount")) != str(amount):
                continue
            if commitment_date and commitment.get("commitment_date") != commitment_date:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_commitments",
                "description": "List commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "Filter by commitment ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "amount": {"type": "string", "description": "Filter by commitment amount"},
                        "commitment_date": {"type": "string", "description": "Filter by commitment date"}
                    },
                    "required": []
                }
            }
        }
