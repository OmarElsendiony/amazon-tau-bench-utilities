import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, employee_id: str,
               investor_type: str, contact_email: str, accreditation_status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate employee exists
        if str(employee_id) not in users:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate investor_type
        valid_types = ["organization", "retail", "high_net_worth"]
        if investor_type not in valid_types:
            raise ValueError(f"Invalid investor_type. Must be one of {valid_types}")
        
        # Validate accreditation_status
        valid_statuses = ["accredited", "non_accredited"]
        if accreditation_status not in valid_statuses:
            raise ValueError(f"Invalid accreditation_status. Must be one of {valid_statuses}")
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": str(investor_id),
            "employee_id": employee_id,
            "name": name,
            "investor_type": investor_type,
            "contact_email": contact_email,
            "accreditation_status": accreditation_status,
            "created_at": timestamp
        }
        
        investors[str(investor_id)] = new_investor
        return json.dumps(new_investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_investor",
                "description": "Create a new investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Investor name"},
                        "employee_id": {"type": "string", "description": "ID of the managing employee"},
                        "investor_type": {"type": "string", "description": "Investor type (organization, retail, high_net_worth)"},
                        "contact_email": {"type": "string", "description": "Contact email"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["name", "employee_id", "investor_type", "contact_email", "accreditation_status"]
                }
            }
        }
