import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: str, name: str, instrument_type: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        
        # Validate instrument type
        valid_types = ["stock", "bond", "derivative", "cash", "other"]
        if instrument_type not in valid_types:
            raise ValueError(f"Invalid instrument type. Must be one of {valid_types}")
        
        # Check if ticker already exists
        for instrument in instruments.values():
            if instrument.get("ticker", "").upper() == ticker.upper():
                raise ValueError(f"Instrument with ticker {ticker} already exists")
        
        instrument_id = generate_id(instruments)
        
        new_instrument = {
            "instrument_id": instrument_id,
            "ticker": ticker.upper(),
            "name": name,
            "instrument_type": instrument_type
        }
        
        instruments[str(instrument_id)] = new_instrument
        return json.dumps(new_instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_instrument",
                "description": "Add a new financial instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Ticker symbol of the instrument"},
                        "name": {"type": "string", "description": "Name of the instrument"},
                        "instrument_type": {"type": "string", "description": "Type of instrument (stock, bond, derivative, cash, other)"}
                    },
                    "required": ["ticker", "name", "instrument_type"]
                }
            }
        }
