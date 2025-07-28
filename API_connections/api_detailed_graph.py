import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import json
import numpy as np

with open("interface_1.json") as f:
    mydict = json.load(f)

def create_api_graph_networkx(data):
    G = nx.DiGraph()
    
    colors = {
        'api': '#4A90E2',
        'input': '#7ED321',
        'output': '#F5A623',
        'input_edge': '#50C878',
        'output_edge': '#FF6B35',
        'explicit_connection': '#000000',
        'implicit_connection': '#9013FE'
    }
    
    node_attrs = {}
    pos = {}
    api_names = list(data["APIs"].keys())
    n_apis = len(api_names)
    radius = max(15, n_apis * 2)
    
    for i, (api_name, api_data) in enumerate(data["APIs"].items()):
        angle = 2 * np.pi * i / n_apis
        api_x = radius * np.cos(angle)
        api_y = radius * np.sin(angle)
        
        G.add_node(api_name)
        pos[api_name] = (api_x, api_y)
        node_attrs[api_name] = {
            'node_type': 'api',
            'color': colors['api'],
            'shape': 'rectangle',
            'size': 3000
        }
        
        unique_inputs = {inp["name"]: inp for inp in api_data["inputs"]}
        unique_outputs = {out["name"]: out for out in api_data["outputs"]}
        
        for j, (field_name, _) in enumerate(unique_inputs.items()):
            node_id = f"{api_name}_input_{field_name}"
            input_angle = angle + (j - (len(unique_inputs) - 1) / 2) * 0.3
            input_radius = radius + 3
            input_x = input_radius * np.cos(input_angle)
            input_y = input_radius * np.sin(input_angle)
            
            G.add_node(node_id)
            pos[node_id] = (input_x, input_y)
            node_attrs[node_id] = {
                'node_type': 'input',
                'color': colors['input'],
                'shape': 'circle',
                'size': 500,
                'label': field_name
            }
            G.add_edge(node_id, api_name,
                       edge_type='input_connection',
                       color=colors['input_edge'])
        
        for j, (field_name, _) in enumerate(unique_outputs.items()):
            node_id = f"{api_name}_output_{field_name}"
            output_angle = angle + (j - (len(unique_outputs) - 1) / 2) * 0.3
            output_radius = radius - 3
            output_x = output_radius * np.cos(output_angle)
            output_y = output_radius * np.sin(output_angle)
            
            G.add_node(node_id)
            pos[node_id] = (output_x, output_y)
            node_attrs[node_id] = {
                'node_type': 'output',
                'color': colors['output'],
                'shape': 'circle',
                'size': 500,
                'label': field_name
            }
            G.add_edge(api_name, node_id,
                       edge_type='output_connection',
                       color=colors['output_edge'])

    if "edges" in data:
        connection_count = {}
        for edge in data["edges"]:
            key = f"{edge['from']}-{edge['to']}"
            connection_count.setdefault(key, []).append(edge)

        for api_pair, edges in connection_count.items():
            edge_to_use = edges[0]
            for edge in edges:
                if edge.get("explicit", True):
                    edge_to_use = edge
                    break
            
            from_api = edge_to_use["from"]
            to_api = edge_to_use["to"]
            output_field = edge_to_use["connections"]["output"]
            input_field = edge_to_use["connections"]["input"]
            is_explicit = edge_to_use.get("explicit", True)
            edge_color = colors['explicit_connection'] if is_explicit else colors['implicit_connection']
            
            from_node = f"{from_api}_output_{output_field}"
            to_node = f"{to_api}_input_{input_field}"
            
            if from_node in G.nodes() and to_node in G.nodes():
                G.add_edge(from_node, to_node,
                           edge_type='api_connection',
                           color=edge_color,
                           label=f"{output_field}→{input_field}",
                           explicit=is_explicit)
    
    return G, pos, node_attrs, colors

def draw_api_graph(G, pos, node_attrs, colors):
    fig, ax = plt.subplots(1, 1, figsize=(24, 24))
    edge_types = {'input_connection': [], 'output_connection': [], 'api_connection': []}
    
    for u, v, data in G.edges(data=True):
        edge_type = data.get('edge_type', 'api_connection')
        edge_types[edge_type].append((u, v, data))
    
    if edge_types['input_connection']:
        edges = [(u, v) for u, v, _ in edge_types['input_connection']]
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                               edge_color=colors['input_edge'],
                               width=2, alpha=0.6,
                               arrowsize=15, arrowstyle='-|>',
                               connectionstyle="arc3,rad=0.1")
    
    if edge_types['output_connection']:
        edges = [(u, v) for u, v, _ in edge_types['output_connection']]
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                               edge_color=colors['output_edge'],
                               width=2, alpha=0.6,
                               arrowsize=15, arrowstyle='-|>',
                               connectionstyle="arc3,rad=0.1")
    
    if edge_types['api_connection']:
        explicit_edges = [(u, v) for u, v, d in edge_types['api_connection'] if d.get('explicit', True)]
        implicit_edges = [(u, v) for u, v, d in edge_types['api_connection'] if not d.get('explicit', True)]
        
        if explicit_edges:
            nx.draw_networkx_edges(G, pos, edgelist=explicit_edges,
                                   edge_color=colors['explicit_connection'],
                                   width=3, alpha=0.8,
                                   arrowsize=20, arrowstyle='-|>',
                                   connectionstyle="arc3,rad=0.2")
        if implicit_edges:
            nx.draw_networkx_edges(G, pos, edgelist=implicit_edges,
                                   edge_color=colors['implicit_connection'],
                                   width=3, alpha=0.8,
                                   arrowsize=20, arrowstyle='-|>',
                                   connectionstyle="arc3,rad=0.3", style='dashed')
    
    for node, attrs in node_attrs.items():
        x, y = pos[node]
        if attrs['node_type'] == 'api':
            rect = FancyBboxPatch((x-2, y-0.8), 4, 1.6,
                                  boxstyle="round,pad=0.1",
                                  facecolor=attrs['color'], edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, node, ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white')
        else:
            circle = Circle((x, y), 0.6, facecolor=attrs['color'],
                            edgecolor='black', linewidth=1)
            ax.add_patch(circle)
            ax.text(x, y, attrs['label'], ha='center', va='center',
                    fontsize=7, fontweight='bold', color='black')
    
    all_x = [x for x, _ in pos.values()]
    all_y = [y for _, y in pos.values()]
    margin = 5
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    ax.set_aspect('equal')
    ax.axis('off')
    
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=colors['api'], markersize=12, label='API'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['input'], markersize=8, label='Input'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['output'], markersize=8, label='Output'),
        plt.Line2D([0], [0], color=colors['explicit_connection'], linewidth=2, label='Explicit'),
        plt.Line2D([0], [0], color=colors['implicit_connection'], linewidth=2, linestyle='--', label='Implicit')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1),
              fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    return fig, ax

# Generate and draw detailed graph
print("Creating improved NetworkX API graph...")
G, pos, node_attrs, colors = create_api_graph_networkx(mydict)
print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

fig, ax = draw_api_graph(G, pos, node_attrs, colors)

# Save only SVG
plt.figure(fig.number)
plt.savefig('api_flow_graph_detailed.svg', bbox_inches='tight', facecolor='white', edgecolor='none')
print("Detailed graph saved as api_flow_graph_detailed.svg")

plt.show()
