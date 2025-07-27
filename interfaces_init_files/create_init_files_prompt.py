

def create_prompt():
    with open('interface_files.txt', 'r') as file:
        interface_files = file.read().strip()
        
    with open('example_init_file.txt', 'r') as file:
        example_init_file = file.read().strip()

    prompt = f"""I am going to give you the names of the files that hold the classes. I want you to create an __init__.py file that targets those files like the example provided below. 
    
    The files are:
    {interface_files}
    
    Example of the __init__.py file:
    {example_init_file}
    """
    
    return prompt

prompt = create_prompt()
with open('create_init_files_prompt.txt', 'w') as file:
    file.write(prompt)
