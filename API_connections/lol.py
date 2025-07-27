import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import json

with open("interface_1.json") as f:
    mydict = json.load(f)

def create_api_graph_networkx(data):
    # Create directed graph
    G = nx.DiGraph()
    
    # Color scheme
    colors = {
        'api': '#4A90E2',           # Nice blue
        'input': '#7ED321',         # Fresh green
        'output': '#F5A623',        # Warm orange
        'input_edge': '#50C878',    # Emerald green
        'output_edge': '#FF6B35',   # Orange red
        'explicit_connection': '#000000',  # Black for explicit connections
        'implicit_connection': '#9013FE'   # Purple for implicit connections
    }
    
    # Node attributes storage
    node_attrs = {}
    pos = {}
    
    # Calculate positions for APIs and their input/output nodes
    api_names = list(data["APIs"].keys())
    api_spacing = 8.0
    
    for i, (api_name, api_data) in enumerate(data["APIs"].items()):
        api_x = i * api_spacing
        api_y = 0
        
        # Add API node
        G.add_node(api_name)
        pos[api_name] = (api_x, api_y)
        node_attrs[api_name] = {
            'node_type': 'api',
            'color': colors['api'],
            'shape': 'rectangle',
            'size': 3000
        }
        
        # Add input nodes (positioned above API)
        input_count = len(api_data["inputs"])
        for j, input_field in enumerate(api_data["inputs"]):
            field_name = input_field["name"]
            node_id = f"{api_name}_input_{field_name}"
            
            # Position inputs above API in a row
            input_x = api_x + (j - (input_count - 1) / 2) * 2.0
            input_y = api_y + 3.0
            
            G.add_node(node_id)
            pos[node_id] = (input_x, input_y)
            node_attrs[node_id] = {
                'node_type': 'input',
                'color': colors['input'],
                'shape': 'circle',
                'size': 800,
                'label': field_name
            }
            
            # Add edge from input to API (input → API)
            G.add_edge(node_id, api_name, 
                      edge_type='input_connection',
                      color=colors['input_edge'])
        
        # Add output nodes (positioned below API)
        output_count = len(api_data["outputs"])
        for j, output_field in enumerate(api_data["outputs"]):
            field_name = output_field["name"]
            node_id = f"{api_name}_output_{field_name}"
            
            # Position outputs below API in a row
            output_x = api_x + (j - (output_count - 1) / 2) * 2.0
            output_y = api_y - 3.0
            
            G.add_node(node_id)
            pos[node_id] = (output_x, output_y)
            node_attrs[node_id] = {
                'node_type': 'output',
                'color': colors['output'],
                'shape': 'circle',
                'size': 800,
                'label': field_name
            }
            
            # Add edge from API to output (API → output)
            G.add_edge(api_name, node_id,
                      edge_type='output_connection',
                      color=colors['output_edge'])
    
    # Add API-to-API connections
    if "edges" in data:
        for edge in data["edges"]:
            from_api = edge["from"]
            to_api = edge["to"]
            output_field = edge["connections"]["output"]
            input_field = edge["connections"]["input"]
            
            is_explicit = edge.get("explicit", True)
            edge_color = colors['explicit_connection'] if is_explicit else colors['implicit_connection']
            
            from_node = f"{from_api}_output_{output_field}"
            to_node = f"{to_api}_input_{input_field}"
            
            G.add_edge(from_node, to_node,
                      edge_type='api_connection',
                      color=edge_color,
                      label=f"{output_field} → {input_field}",
                      explicit=is_explicit)
    
    return G, pos, node_attrs, colors

def draw_api_graph(G, pos, node_attrs, colors):
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Draw edges by type
    edge_types = {
        'input_connection': [],
        'output_connection': [],
        'api_connection': []
    }
    
    # Group edges by type
    for u, v, data in G.edges(data=True):
        edge_type = data.get('edge_type', 'api_connection')
        edge_types[edge_type].append((u, v, data))
    
    # Draw input connections (input → API) with LARGE arrows
    if edge_types['input_connection']:
        edges = [(u, v) for u, v, _ in edge_types['input_connection']]
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                              edge_color=colors['input_edge'],
                              width=4, alpha=0.9,
                              arrowsize=30, 
                              arrowstyle='-|>',  # More prominent arrow style
                              connectionstyle="arc3,rad=0",
                              min_source_margin=20,
                              min_target_margin=20)
    
    # Draw output connections (API → output) with LARGE arrows
    if edge_types['output_connection']:
        edges = [(u, v) for u, v, _ in edge_types['output_connection']]
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                              edge_color=colors['output_edge'],
                              width=4, alpha=0.9,
                              arrowsize=30,
                              arrowstyle='-|>',  # More prominent arrow style
                              connectionstyle="arc3,rad=0",
                              min_source_margin=20,
                              min_target_margin=20)
    
    # Draw API-to-API connections with VERY LARGE arrows
    if edge_types['api_connection']:
        explicit_edges = [(u, v) for u, v, data in edge_types['api_connection'] if data.get('explicit', True)]
        implicit_edges = [(u, v) for u, v, data in edge_types['api_connection'] if not data.get('explicit', True)]
        
        if explicit_edges:
            nx.draw_networkx_edges(G, pos, edgelist=explicit_edges,
                                  edge_color=colors['explicit_connection'],
                                  width=5, alpha=1.0,
                                  arrowsize=40,  # Even bigger arrows
                                  arrowstyle='-|>',  # Most prominent arrow style
                                  connectionstyle="arc3,rad=0.1",
                                  min_source_margin=25,
                                  min_target_margin=25)
        
        if implicit_edges:
            nx.draw_networkx_edges(G, pos, edgelist=implicit_edges,
                                  edge_color=colors['implicit_connection'],
                                  width=5, alpha=1.0,
                                  arrowsize=40,  # Even bigger arrows
                                  arrowstyle='-|>',  # Most prominent arrow style
                                  connectionstyle="arc3,rad=0.1",
                                  min_source_margin=25,
                                  min_target_margin=25)
    
    # Draw nodes by type
    for node, attrs in node_attrs.items():
        x, y = pos[node]
        
        if attrs['node_type'] == 'api':
            # Draw rectangle for API
            rect = FancyBboxPatch((x-1.5, y-0.5), 3, 1,
                                 boxstyle="round,pad=0.1",
                                 facecolor=attrs['color'],
                                 edgecolor='black',
                                 linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, node, ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')
            
        else:
            # Draw circle for input/output
            circle = plt.Circle((x, y), 0.4,
                               facecolor=attrs['color'],
                               edgecolor='black',
                               linewidth=1.5)
            ax.add_patch(circle)
            ax.text(x, y, attrs['label'], ha='center', va='center',
                   fontsize=10, fontweight='bold', color='black')
    
    # Add edge labels for API connections
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        if data.get('edge_type') == 'api_connection':
            edge_labels[(u, v)] = data.get('label', '')
    
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                    font_size=10, font_color='black',
                                    bbox=dict(boxstyle='round,pad=0.2', 
                                            facecolor='white', alpha=0.8))
    
    # Set axis properties
    ax.set_xlim(min(x for x, y in pos.values()) - 2, 
                max(x for x, y in pos.values()) + 2)
    ax.set_ylim(min(y for x, y in pos.values()) - 2, 
                max(y for x, y in pos.values()) + 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title and legend
    # plt.title('API Flow Graph (NetworkX)', fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=colors['api'], 
                  markersize=15, label='API'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['input'], 
                  markersize=10, label='Input'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['output'], 
                  markersize=10, label='Output'),
        plt.Line2D([0], [0], color=colors['explicit_connection'], linewidth=3, 
                  label='Explicit Connection'),
        plt.Line2D([0], [0], color=colors['implicit_connection'], linewidth=3, 
                  label='Implicit Connection')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    return fig, ax

# Create and visualize the graph
print("Creating NetworkX API graph...")
G, pos, node_attrs, colors = create_api_graph_networkx(mydict)

print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Draw the graph
fig, ax = draw_api_graph(G, pos, node_attrs, colors)

# Save the figure
plt.savefig('api_flow_graph_networkx.png', dpi=300, bbox_inches='tight')
plt.savefig('api_flow_graph_networkx.svg', bbox_inches='tight')
print("Graph saved as api_flow_graph_networkx.png and api_flow_graph_networkx.svg")

# Show the plot
plt.show()

# Print graph information
print("\nGraph Information:")
print(f"Nodes: {list(G.nodes())}")
print(f"Edges: {list(G.edges())}")

# Print node positions
print("\nNode Positions:")
for node, position in pos.items():
    print(f"{node}: {position}")
