import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateNewCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               commitment_amount: str, currency: str, commitment_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": commitment_amount,
            "currency": currency,
            "commitment_date": commitment_date,
            "status": "pending",
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps(new_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_commitment",
                "description": "Create a new commitment for an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "string", "description": "Amount of the commitment"},
                        "currency": {"type": "string", "description": "Currency of the commitment (USD, EUR, GBP, NGN)"},
                        "commitment_date": {"type": "string", "description": "Date of the commitment in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "currency", "commitment_date"]
                }
            }
        }
