import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_instruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: Optional[str] = None,
               name: Optional[str] = None, instrument_type: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if ticker and instrument.get("ticker", "").lower() != ticker.lower():
                continue
            if name and name.lower() not in instrument.get("name", "").lower():
                continue
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments",
                "description": "Get instruments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"},
                        "name": {"type": "string", "description": "Filter by instrument name (partial match)"},
                        "instrument_type": {"type": "string", "description": "Filter by instrument type (stock, bond, derivative, cash, other)"}
                    },
                    "required": []
                }
            }
        }
