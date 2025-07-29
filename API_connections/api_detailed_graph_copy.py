import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import json
import numpy as np

# Load the JSON data
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
        'explicit_connection': '#9013FE',
        'implicit_connection': '#9013FE'
    }
    
    node_attrs = {}
    pos = {}
    api_names = list(data["APIs"].keys())
    n_apis = len(api_names)
    main_radius = max(25, n_apis * 6)
    
    for i, (api_name, api_data) in enumerate(data["APIs"].items()):
        angle = 2 * np.pi * i / n_apis
        api_x = main_radius * np.cos(angle)
        api_y = main_radius * np.sin(angle)
        
        G.add_node(api_name)
        pos[api_name] = (api_x, api_y)
        node_attrs[api_name] = {
            'node_type': 'api',
            'color': colors['api'],
            'shape': 'rectangle'
        }
        
        attributes = []
        for inp in api_data.get("inputs", []):
            attributes.append({'name': inp['name'], 'type': 'input'})
        for out in api_data.get("outputs", []):
            attributes.append({'name': out['name'], 'type': 'output'})
        
        unique_attributes = {f"{attr['type']}_{attr['name']}": attr for attr in attributes}
        n_attrs = len(unique_attributes)
        attr_radius = 5.0 

        for j, (key, attr) in enumerate(unique_attributes.items()):
            attr_angle = 2 * np.pi * j / n_attrs
            attr_x = api_x + attr_radius * np.cos(attr_angle)
            attr_y = api_y + attr_radius * np.sin(attr_angle)
            
            field_name = attr['name']
            node_type = attr['type']
            node_id = f"{api_name}_{node_type}_{field_name}"
            
            G.add_node(node_id)
            pos[node_id] = (attr_x, attr_y)
            node_attrs[node_id] = {
                'node_type': node_type,
                'color': colors[node_type],
                'shape': 'circle',
                'label': field_name
            }
            
            if node_type == 'input':
                G.add_edge(node_id, api_name,
                           edge_type='input_connection',
                           color=colors['input_edge'])
            else:
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

    def calculate_boundary_point(origin_pos, target_pos, target_node_attrs):
        vec_from_target = np.array(origin_pos) - np.array(target_pos)
        
        if np.linalg.norm(vec_from_target) == 0:
            return np.array(target_pos)

        if target_node_attrs['shape'] == 'circle':
            radius = 0.5
            return np.array(target_pos) + vec_from_target / np.linalg.norm(vec_from_target) * radius
        elif target_node_attrs['shape'] == 'rectangle':
            w, h = 2.1, 0.7
            dx, dy = vec_from_target
            if abs(dy) * w > abs(dx) * h:
                scale = h / abs(dy)
            else:
                scale = w / abs(dx)
            return np.array(target_pos) + vec_from_target * scale

        return np.array(target_pos)

    for u, v, data in G.edges(data=True):
        source_pos = np.array(pos[u])
        target_pos = np.array(pos[v])
        
        start_point = calculate_boundary_point(target_pos, source_pos, node_attrs[u])
        end_point = calculate_boundary_point(source_pos, target_pos, node_attrs[v])

        edge_type = data.get('edge_type', 'api_connection')
        color = data.get('color')
        
        connectionstyle = "arc3,rad=0.1"
        arrowstyle = '-|>'
        linewidth = 1.5
        alpha = 0.6
        mutation_scale = 12
        linestyle = 'solid'
        
        if edge_type == 'api_connection':
            is_explicit = data.get('explicit', True)
            connectionstyle = "arc3,rad=0.2" if is_explicit else "arc3,rad=0.3"
            # linestyle = 'solid' if is_explicit else 'dashed'
            linestyle = 'dashed'
            linewidth = 1.5
            alpha = 0.8
            mutation_scale = 20
        
        arrow = FancyArrowPatch(
            posA=tuple(start_point), posB=tuple(end_point),
            arrowstyle=arrowstyle, connectionstyle=connectionstyle,
            color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha,
            mutation_scale=mutation_scale, zorder=1
        )
        ax.add_patch(arrow)

        # if edge_type == 'api_connection' and 'label' in data:
        #     rad = 0.2 if data.get('explicit', True) else 0.3
        #     x1, y1 = start_point
        #     x2, y2 = end_point
            
        #     mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        #     edge_vec_x, edge_vec_y = x2 - x1, y2 - y1
        #     edge_length = np.sqrt(edge_vec_x**2 + edge_vec_y**2)

        #     if edge_length > 0:
        #         perp_x = -edge_vec_y / edge_length
        #         perp_y = edge_vec_x / edge_length
        #         arc_offset = rad * edge_length
        #         control_x = mid_x + perp_x * arc_offset
        #         control_y = mid_y + perp_y * arc_offset
                
        #         label_x = (mid_x + control_x) / 2
        #         label_y = (mid_y + control_y) / 2
                
        #         is_explicit = data.get('explicit', True)
        #         label_color = 'black' if is_explicit else 'purple'
        #         bbox_props = dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9, edgecolor=label_color)
                
        #         ax.text(label_x, label_y, data['label'], ha='center', va='center',
        #                 fontsize=6, fontweight='bold', color=label_color,
        #                 bbox=bbox_props, zorder=3)

    for node, attrs in node_attrs.items():
        x, y = pos[node]
        if attrs['node_type'] == 'api':
            rect = FancyBboxPatch((x-2.1, y-0.7), 4.2, 1.4,
                                  boxstyle="round,pad=0.05",
                                  facecolor=attrs['color'], edgecolor='black', 
                                  linewidth=2, zorder=2)
            ax.add_patch(rect)
            # ↓↓↓ Updated here ↓↓↓
            ax.text(x, y, node, ha='center', va='center',
                    fontsize=6, fontweight='normal', color='black', zorder=3)
        else:
            circle = Circle((x, y), 0.5, facecolor=attrs['color'],
                            edgecolor='black', linewidth=1, zorder=2)
            ax.add_patch(circle)
            ax.text(x, y, attrs['label'], ha='center', va='center',
                    fontsize=5, fontweight='bold', color='black', zorder=3)
    
    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    margin = 5
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    ax.set_aspect('equal')
    ax.axis('off')
    
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', label='API', markerfacecolor=colors['api'], markersize=12),
        plt.Line2D([0], [0], marker='o', color='w', label='Input', markerfacecolor=colors['input'], markersize=6),
        plt.Line2D([0], [0], marker='o', color='w', label='Output', markerfacecolor=colors['output'], markersize=6),
        plt.Line2D([0], [0], color=colors['explicit_connection'], lw=2, linestyle='--', label='Connection'),
        # plt.Line2D([0], [0], color=colors['implicit_connection'], lw=2, linestyle='--', label='Implicit Connection')
    ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    return fig, ax

# --- Main execution block ---
print("Creating improved NetworkX API graph...")
G, pos, node_attrs, colors = create_api_graph_networkx(mydict)
print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

fig, ax = draw_api_graph(G, pos, node_attrs, colors)

plt.figure(fig.number)
plt.savefig('api_flow_graph_detailed.svg', bbox_inches='tight', facecolor='white', edgecolor='none')
print("Detailed graph saved as api_flow_graph_detailed.svg")
