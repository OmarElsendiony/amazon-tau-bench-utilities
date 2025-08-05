

# create the ultimate prompt for the API implementation
def create_prompt():
    with open('examples_tools.txt', 'r') as f:
        examples_tools = f.read()

    with open('required_tools.txt', 'r') as f:
        required_tools = f.read()

    with open('db_schema.txt', 'r') as f:
        db_schema = f.read()

    prompt = f"""
I have a set of tools that I use to interact with a DB in a json format. These tools allow me to perform various operations such as creating, reading, updating, and deleting records in the database. Those tools are functions that take parameters and return a value in json format.
Your task is to create for me the tools. Each tool is a class that comprises of two functions: one for the implementation of the tool and another for the schema of the tool. The implementation function should return a json string that represents the result of the operation, while the schema function should return a dictionary that describes the parameters and their types. The schema function should also include a description of the tool and its parameters. I will provide you with examples of tools with their implementations and schemas, and you should use them as a reference to create your own tools. Also, I will provide the database schema for you to use as a reference for the parameters and their types.

# Database schema:
{db_schema}

# Examples of a tool implementation and schema:
{examples_tools}

# Required tools:
{required_tools}

Please create the tools based on the examples and the database schema. 

Notes: 
- assign this timestamp to the created_at and updated_at fields: "2025-10-01T00:00:00ZZ".
- All IDs are strings, not integers.
- Use the generate_id function to generate unique IDs for the records.
- Each tool should have its own imports and utility functions without being shared across tools.
- The tools should be implemented in a way that they can be used independently.

Your generated tools should be in a bash script that can be executed to create them in files that hold the same name as the class name. Each file should contain the class definition and its methods. The files should be named as follows: {{tool_name}}.py, where {{tool_name}} is the name of the tool class. Take care that all names should be in snake_case format.
    """
    return prompt


created_prompt = create_prompt()
with open('created_prompt.txt', 'w') as f:
    f.write(created_prompt)
