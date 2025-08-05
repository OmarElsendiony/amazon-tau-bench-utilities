import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, name: str, 
               contact_email: str, accreditation_status: str) -> str:
        
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate accreditation status
        valid_statuses = ["accredited", "non_accredited"]
        if accreditation_status not in valid_statuses:
            raise ValueError(f"Invalid accreditation status. Must be one of {valid_statuses}")
        
        # Update investor details
        investor = investors[str(investor_id)]
        investor["name"] = name
        investor["contact_email"] = contact_email
        investor["accreditation_status"] = accreditation_status
        
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_details",
                "description": "Update investor details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "name": {"type": "string", "description": "New name of the investor"},
                        "contact_email": {"type": "string", "description": "New contact email of the investor"},
                        "accreditation_status": {"type": "string", "description": "New accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["investor_id", "name", "contact_email", "accreditation_status"]
                }
            }
        }
