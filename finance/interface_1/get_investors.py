import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_investors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None,
               investor_type: Optional[str] = None, accreditation_status: Optional[str] = None,
               name: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            if investor_type and investor.get("investor_type") != investor_type:
                continue
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investors",
                "description": "Get investors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "investor_type": {"type": "string", "description": "Filter by investor type (organization, retail, high_net_worth)"},
                        "accreditation_status": {"type": "string", "description": "Filter by accreditation status (accredited, non_accredited)"},
                        "name": {"type": "string", "description": "Filter by investor name (partial match)"}
                    },
                    "required": []
                }
            }
        }
