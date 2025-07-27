
def api_prompt():
    with open('db_schema.txt', 'r') as file:
        db_schema = file.read()
    
    with open('api_documentation.txt', 'r') as file:
        api_documentation = file.read()
    
    with open('json_format.txt', 'r') as file:
        json_format = file.read()
    
    prompt = f"""You are an expert in managing API connections. We have some APIs that reside within an interface. Those APIs have input and output parameters. I want you to determine the connections between those APIs through their parameters either explicitly or implicitly. Your task is to ensure that all API connections depict correct relations that are conveyed through the db schema or the API documentation. You will be provided with the API documentation and the db schema. Your goal is to identify and describe the relationships between the APIs based on their parameters and the data they exchange but you have to adhere to the json format provided below where you add all the inputs and outputs of an api, then determine its connections implicitly or explicitly with others.
    
    DB schema:
    {db_schema}
    
    API documentation:
    {api_documentation}
    
    Please provide the API connections in the following JSON format:
    {json_format}
"""

    prompt = prompt.format(db_schema=db_schema, api_documentation=api_documentation, json_format=json_format)
    return prompt


prompt = api_prompt()

with open('api_connection_prompt.txt', 'w') as file:
    file.write(prompt)
