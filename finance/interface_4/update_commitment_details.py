import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateCommitmentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str,
               commitment_amount: str, status: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        commitment = commitments[str(commitment_id)]
        commitment["commitment_amount"] = commitment_amount
        commitment["status"] = status
        commitment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_commitment_details",
                "description": "Update commitment details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "commitment_amount": {"type": "string", "description": "Updated commitment amount"},
                        "status": {"type": "string", "description": "Updated status (pending, fulfilled)"}
                    },
                    "required": ["commitment_id", "commitment_amount", "status"]
                }
            }
        }
