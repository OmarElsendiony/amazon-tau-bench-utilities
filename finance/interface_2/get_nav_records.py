import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetNAVRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        nav_records = data.get("nav_records", {})
        results = []
        
        for nav in nav_records.values():
            # Apply filters
            skip_record = False
            for key, value in filters.items():
                if key in nav and nav.get(key) != value:
                    skip_record = True
                    break
            
            if not skip_record:
                results.append(nav)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_records",
                "description": "Get NAV records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria for NAV records"}
                    },
                    "required": ["filters"]
                }
            }
        }
