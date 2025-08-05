While creating the interface document, specify the type of the argument as well as mention which arguments are optional so that we should leave very little room for the LLM to make any assumption about your API 
Also add a very brief line about what the function will do:
Example:

add_device
add_device(device_type: str, room_id: str, home_id: str, width_ft: float, length_ft: float, price: float, daily_rated_power_consumption_kWh: float, optional: brightness_level: str, optional: color: str, optional: insurance_expiry_date: str)
{"device_id": str, "success": True}
Adds a new device; if a bulb, also creates smart bulb entry

The prompt in create_prompt.txt was given to ChatGPT o4-mini-high model and the response was copied in parse_response_and_ceate_APIs/generate_tools.sh 
Then we ran these: 


chmod +x parse_response_and_create_APIs/generate_tools.sh

ash generate_tools.sh