import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckCommitmentFulfillmentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        status = commitment.get("status", "pending")
        
        return json.dumps({"status": status})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_commitment_fulfillment_status",
                "description": "Check the fulfillment status of a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
