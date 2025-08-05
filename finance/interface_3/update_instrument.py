import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, ticker: Optional[str] = None, 
               name: Optional[str] = None, instrument_type: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate instrument type if provided
        if instrument_type:
            valid_types = ["stock", "bond", "derivative", "cash", "other"]
            if instrument_type not in valid_types:
                raise ValueError(f"Invalid instrument type. Must be one of {valid_types}")
        
        instrument = instruments[str(instrument_id)]
        
        # Update fields if provided
        if ticker is not None:
            instrument["ticker"] = ticker
        if name is not None:
            instrument["name"] = name
        if instrument_type is not None:
            instrument["instrument_type"] = instrument_type
        
        return json.dumps(instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Update an instrument's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "ticker": {"type": "string", "description": "Instrument ticker symbol"},
                        "name": {"type": "string", "description": "Instrument name"},
                        "instrument_type": {"type": "string", "description": "Type of instrument (stock, bond, derivative, cash, other)"}
                    },
                    "required": ["instrument_id"]
                }
            }
        }
