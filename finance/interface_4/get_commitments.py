import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        if not filters:
            filters = {}
        
        for commitment in commitments.values():
            # Apply filters
            if filters.get("commitment_id") and commitment.get("commitment_id") != filters["commitment_id"]:
                continue
            if filters.get("fund_id") and commitment.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and commitment.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("currency") and commitment.get("currency") != filters["currency"]:
                continue
            if filters.get("status") and commitment.get("status") != filters["status"]:
                continue
            if filters.get("commitment_date") and commitment.get("commitment_date") != filters["commitment_date"]:
                continue
            
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (commitment_id, fund_id, investor_id, currency, status, commitment_date)"
                        }
                    },
                    "required": []
                }
            }
        }
