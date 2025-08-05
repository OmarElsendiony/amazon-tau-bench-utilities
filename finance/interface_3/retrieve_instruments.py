import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for instrument in instruments.values():
            # Apply filters
            if filters.get("instrument_id") and str(instrument.get("instrument_id")) != str(filters["instrument_id"]):
                continue
            if filters.get("ticker") and instrument.get("ticker", "").upper() != filters["ticker"].upper():
                continue
            if filters.get("name") and filters["name"].lower() not in instrument.get("name", "").lower():
                continue
            if filters.get("instrument_type") and instrument.get("instrument_type") != filters["instrument_type"]:
                continue
                
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instruments",
                "description": "Retrieve instruments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                                "ticker": {"type": "string", "description": "Filter by ticker symbol"},
                                "name": {"type": "string", "description": "Filter by name (partial match)"},
                                "instrument_type": {"type": "string", "description": "Filter by instrument type (stock, bond, derivative, cash, other)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
