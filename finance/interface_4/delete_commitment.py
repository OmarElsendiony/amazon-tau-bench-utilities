import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        deleted_commitment = commitments.pop(str(commitment_id))
        return json.dumps(deleted_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_commitment",
                "description": "Delete a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment to delete"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
