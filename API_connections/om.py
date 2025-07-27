import graphviz

mydict = {
    "APIs": {
        "getcompany": {
            "inputs": [
                {
                    "name": "company_id",
                    "type": "string",
                    "required": True,
                    "description": "The unique identifier for the company."
                }
            ],
            "outputs": [
                {
                    "name": "company_name",
                    "type": "string",
                    "description": "The name of the company."
                },
                {
                    "name": "company_address",
                    "type": "string", 
                    "description": "The address of the company."
                },
                {
                    "name": "company_id",
                    "type": "string",
                    "description": "The unique identifier for the company."
                }
            ]
        },
        "getUser": {
            "inputs": [
                {
                    "name": "user_id",
                    "type": "string",
                    "required": True,
                    "description": "The unique identifier for the user."
                },
                {
                    "name": "company_id",
                    "type": "string",
                    "required": True,
                    "description": "The company ID associated with the user."
                }
            ],
            "outputs": [
                {
                    "name": "user_name",
                    "type": "string",
                    "description": "The name of the user."
                },
                {
                    "name": "company_id",
                    "type": "string",
                    "description": "The company ID of the user."
                }
            ]
        }
    },
    "edges": [
        {
            "from": "getUser",
            "to": "getcompany",
            "connections": {
                "output": "company_id",
                "input": "company_id"
            },
            "explicit": False  # Black edge - explicit connection
        },
        {
            "from": "getcompany",
            "to": "getUser",
            "connections": {
                "output": "company_id",
                "input": "company_id"
            },
            "explicit": False  # Purple edge - implicit connection
        }
    ]
}

def create_api_graph(data):
    # Create a directed graph
    dot = graphviz.Digraph(comment='API Flow Graph')
    dot.attr(rankdir='TB', splines='curved')  # Added curved edges
    
    # Color scheme - improved colors
    colors = {
        'api': '#4A90E2',           # Nice blue
        'input': '#7ED321',         # Fresh green
        'output': '#F5A623',        # Warm orange
        'input_edge': '#50C878',    # Emerald green
        'output_edge': '#FF6B35',   # Orange red
        'explicit_connection': '#000000',  # Black for explicit connections
        'implicit_connection': '#9013FE'   # Purple for implicit connections
    }
    
    # Add API nodes (rectangle shape) - fixed size
    for api_name in data["APIs"].keys():
        dot.node(api_name, api_name, 
                shape='rectangle',  # Changed to rectangle
                style='filled', 
                fillcolor=colors['api'],
                fontweight='bold',
                width='3.0',  # Fixed width
                height='1.5',  # Fixed height
                fixedsize='true')  # Force fixed size
    
    # Add input and output nodes for each API - positioned close to API
    for api_name, api_data in data["APIs"].items():
        # Add input nodes - ALWAYS point TO the API (consistent direction)
        for input_field in api_data["inputs"]:
            field_name = input_field["name"]
            node_id = f"{api_name}_input_{field_name}"
            
            dot.node(node_id, 
                    f"{field_name}", 
                    shape='circle',
                    style='filled',
                    fillcolor=colors['input'],
                    fontsize='10',
                    width='1.0',  # Fixed width
                    height='1.0',  # Fixed height
                    fixedsize='true')  # Force fixed size
            
            # ALWAYS connect input TO API (removed the reversal logic)
            dot.edge(node_id, api_name, color=colors['input_edge'], penwidth='2')
        
        # Add output nodes - ALWAYS point FROM the API  
        for output_field in api_data["outputs"]:
            field_name = output_field["name"]
            node_id = f"{api_name}_output_{field_name}"
            
            dot.node(node_id,
                    f"{field_name}",
                    shape='circle', 
                    style='filled',
                    fillcolor=colors['output'],
                    fontsize='10',
                    width='1.0',  # Fixed width
                    height='1.0',  # Fixed height
                    fixedsize='true')  # Force fixed size
            
            # Connect API to output
            dot.edge(api_name, node_id, color=colors['output_edge'], penwidth='2')
    
    # Add edges between APIs based on connections
    if "edges" in data:
        for edge in data["edges"]:
            from_api = edge["from"]
            to_api = edge["to"]
            output_field = edge["connections"]["output"]
            input_field = edge["connections"]["input"]
            
            # Check if connection is explicit (default to True if not specified)
            is_explicit = edge.get("explicit", True)
            
            # Create edge between output of source API and input of target API
            from_node = f"{from_api}_output_{output_field}"
            to_node = f"{to_api}_input_{input_field}"
            
            # Choose color based on explicit flag
            edge_color = colors['explicit_connection'] if is_explicit else colors['implicit_connection']
            
            dot.edge(from_node, to_node, 
                    label=f"  {output_field} → {input_field}  ",
                    color=edge_color,
                    penwidth='3',
                    fontsize='14',
                    fontcolor='black',
                    labelfontsize='14',
                    labeldistance='2.0',
                    labelangle='0')
    
    return dot

# Create and render the graph
graph = create_api_graph(mydict)

# Render the graph
print("Rendering graph...")
graph.render('api_flow_graph', format='svg', cleanup=True)
print("Graph saved as api_flow_graph.svg")

# Display the source code for inspection
print("\nGraphviz source:")
print(graph.source)
