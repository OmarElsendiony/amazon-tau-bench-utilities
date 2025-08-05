import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFilteredInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        investors = data.get("investors", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for investor in investors.values():
            # Apply filters
            if filters.get("investor_id") and str(investor.get("investor_id")) != str(filters["investor_id"]):
                continue
            if filters.get("employee_id") and str(investor.get("employee_id")) != str(filters["employee_id"]):
                continue
            if filters.get("name") and filters["name"].lower() not in investor.get("name", "").lower():
                continue
            if filters.get("investor_type") and investor.get("investor_type") != filters["investor_type"]:
                continue
            if filters.get("contact_email") and investor.get("contact_email", "").lower() != filters["contact_email"].lower():
                continue
            if filters.get("accreditation_status") and investor.get("accreditation_status") != filters["accreditation_status"]:
                continue
                
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Get investors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "investor_id": {"type": "string", "description": "Filter by investor ID"},
                                "employee_id": {"type": "string", "description": "Filter by employee ID"},
                                "name": {"type": "string", "description": "Filter by name (partial match)"},
                                "investor_type": {"type": "string", "description": "Filter by investor type (organization, retail, high_net_worth)"},
                                "contact_email": {"type": "string", "description": "Filter by contact email"},
                                "accreditation_status": {"type": "string", "description": "Filter by accreditation status (accredited, non_accredited)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
