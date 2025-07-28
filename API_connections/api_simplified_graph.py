import json
import graphviz
from pathlib import Path

def create_graphviz_api_graph(data, output_name="api_connections"):
    """
    Create a simplified API connection graph using Graphviz
    """
    # Create a new directed graph
    dot = graphviz.Digraph(comment='API Connections')
    
    # Set graph attributes for better layout and complete SVG rendering
    dot.attr(rankdir='TB')  # Top to Bottom layout
    dot.attr(splines='curved')  # Use curved splines for smoother edges
    dot.attr(nodesep='1.2')  # Increased horizontal separation
    dot.attr(ranksep='2.0')  # Increased vertical separation
    dot.attr(bgcolor='white')
    
    # Remove size constraints that can cause clipping
    # dot.attr(size='12,16')  # Remove this line
    # dot.attr(dpi='96')      # Remove this line
    
    # Use margin instead of size constraints
    dot.attr(margin='1.0')
    dot.attr(pad='1.0')
    
    # Set default node attributes
    dot.attr('node', 
             shape='box',
             style='rounded,filled',
             fillcolor='lightblue',
             color='black',
             fontname='Arial',  # Use a more standard font
             fontsize='11',
             margin='0.4,0.2',
             width='2.0',   # Reduced width
             height='0.8')  # Reduced height
    
    # Set default edge attributes
    dot.attr('edge',
             fontname='Arial',
             fontsize='9',
             color='black',
             arrowsize='0.8',
             labeldistance='2.0',  # Distance of label from edge
             labelangle='0',       # Keep labels horizontal
             labelfloat='true')    # Allow labels to float for better positioning
    
    # Add API nodes
    api_names = list(data["APIs"].keys())
    
    # Group APIs by type for better layout
    read_apis = []
    create_update_apis = []
    
    for api_name in api_names:
        # Simple heuristic to group APIs
        if any(keyword in api_name.lower() for keyword in ['get', 'search', 'list', 'find']):
            read_apis.append(api_name)
        else:
            create_update_apis.append(api_name)
    
    # Add read API nodes
    for api_name in read_apis:
        display_name = format_api_name(api_name)
        dot.node(api_name, 
                display_name,
                fillcolor='lightgreen',
                tooltip=f'Read API: {api_name}')
    
    # Add create/update API nodes
    for api_name in create_update_apis:
        display_name = format_api_name(api_name)
        dot.node(api_name, 
                display_name,
                fillcolor='lightcoral',
                tooltip=f'Create/Update API: {api_name}')
    
    # Add edges based on API connections
    add_edges_to_graph(dot, data)
    
    return dot

def create_hierarchical_layout(data, output_name="api_hierarchy"):
    """
    Create a hierarchical layout based on API dependencies
    """
    dot = graphviz.Digraph(comment='API Hierarchy')
    
    # Set graph attributes for hierarchical layout
    dot.attr(rankdir='TB')
    dot.attr(splines='curved')  # Use curved splines for smoother edges
    dot.attr(nodesep='1.0')
    dot.attr(ranksep='1.5')
    dot.attr(bgcolor='white')
    dot.attr(margin='1.0')
    dot.attr(pad='1.0')
    
    # Remove size constraints
    # dot.attr(size='14,18')
    # dot.attr(dpi='96')
    
    # Set node attributes
    dot.attr('node',
             shape='box',
             style='rounded,filled',
             fontname='Arial',
             fontsize='10',
             margin='0.3,0.2')
    
    # Set edge attributes
    dot.attr('edge',
             fontname='Arial',
             fontsize='8',
             arrowsize='0.7',
             labeldistance='2.0',
             labelangle='0',
             labelfloat='true')
    
    # Analyze API dependencies to create layers
    source_apis, transformer_apis, consumer_apis = categorize_apis(data)
    
    # Add nodes with proper clustering
    add_clustered_nodes(dot, source_apis, transformer_apis, consumer_apis)
    
    # Add edges
    add_edges_to_graph(dot, data, simplified=True)
    
    return dot

def format_api_name(api_name):
    """Format API name for better display"""
    display_name = api_name.replace('_', ' ').title()
    
    # Handle long names by splitting intelligently
    if len(display_name) > 18:
        words = display_name.split()
        if len(words) > 2:
            # Find best split point
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            
            # Ensure neither line is too long
            if len(line1) > 15 or len(line2) > 15:
                # Try different split
                for i in range(1, len(words)):
                    line1 = ' '.join(words[:i])
                    line2 = ' '.join(words[i:])
                    if len(line1) <= 15 and len(line2) <= 15:
                        break
            
            display_name = f"{line1}\\n{line2}"
        elif len(display_name) > 25:
            # Single long word, truncate with ellipsis
            display_name = display_name[:22] + "..."
    
    return display_name

def add_edges_to_graph(dot, data, simplified=False):
    """Add edges to the graph, avoiding duplicates"""
    if "edges" not in data:
        return
    
    connections = {}
    
    for edge in data["edges"]:
        from_api = edge["from"]
        to_api = edge["to"]
        is_explicit = edge.get("explicit", True)
        
        connection_key = f"{from_api}->{to_api}"
        
        if connection_key not in connections:
            connections[connection_key] = {
                'explicit': is_explicit,
                'output': edge["connections"]["output"],
                'input': edge["connections"]["input"]
            }
        elif is_explicit and not connections[connection_key]['explicit']:
            connections[connection_key] = {
                'explicit': is_explicit,
                'output': edge["connections"]["output"],
                'input': edge["connections"]["input"]
            }
    
    # Add edges to graph
    for connection_key, conn_info in connections.items():
        from_api, to_api = connection_key.split('->')
        
        if simplified:
            # Simple edges for hierarchical view
            if conn_info['explicit']:
                dot.edge(from_api, to_api, color='black', penwidth='1.5')
            else:
                dot.edge(from_api, to_api, color='purple', style='dashed', penwidth='1.0')
        else:
            # Detailed edges with labels
            edge_label = create_edge_label(conn_info['output'], conn_info['input'])
            
            if conn_info['explicit']:
                dot.edge(from_api, to_api,
                        label=edge_label,
                        color='black',
                        style='solid',
                        penwidth='1.5',
                        tooltip=f'Explicit: {conn_info["output"]} → {conn_info["input"]}')
            else:
                dot.edge(from_api, to_api,
                        label=edge_label,
                        color='purple',
                        style='dashed',
                        penwidth='1.5',
                        tooltip=f'Implicit: {conn_info["output"]} → {conn_info["input"]}')

def create_edge_label(output_field, input_field):
    """Create a clean edge label without truncation"""
    if output_field == input_field:
        # Same field name, show it in full but break long names
        if len(output_field) > 15:
            # Split long field names into multiple lines
            words = output_field.replace('_', ' ').split()
            if len(words) > 1:
                mid = len(words) // 2
                line1 = ' '.join(words[:mid])
                line2 = ' '.join(words[mid:])
                return f"{line1}\\n{line2}"
        return output_field.replace('_', ' ')
    else:
        # Different field names, show full names with arrow
        out_formatted = output_field.replace('_', ' ')
        in_formatted = input_field.replace('_', ' ')
        
        # If combined length is very long, put on separate lines
        if len(out_formatted + in_formatted) > 20:
            return f"{out_formatted}\\n↓\\n{in_formatted}"
        else:
            return f"{out_formatted} → {in_formatted}"

def categorize_apis(data):
    """Categorize APIs into source, transformer, and consumer types"""
    api_names = set(data["APIs"].keys())
    source_apis = set()
    consumer_apis = set()
    transformer_apis = set()
    
    if "edges" in data:
        from_apis = set()
        to_apis = set()
        
        for edge in data["edges"]:
            from_apis.add(edge["from"])
            to_apis.add(edge["to"])
        
        for api in api_names:
            is_source = api in from_apis
            is_consumer = api in to_apis
            
            if is_source and is_consumer:
                transformer_apis.add(api)
            elif is_source:
                source_apis.add(api)
            elif is_consumer:
                consumer_apis.add(api)
            else:
                transformer_apis.add(api)
    else:
        # If no edges, categorize all as transformers
        transformer_apis = api_names
    
    return source_apis, transformer_apis, consumer_apis

def add_clustered_nodes(dot, source_apis, transformer_apis, consumer_apis):
    """Add nodes with clustering"""
    # Add source APIs
    if source_apis:
        with dot.subgraph(name='cluster_sources') as sources:
            sources.attr(label='Data Sources', fontsize='12', style='bold')
            sources.attr(color='green', style='rounded')
            
            for api in source_apis:
                display_name = format_api_name(api)
                sources.node(api, display_name, fillcolor='lightgreen')
    
    # Add transformer APIs
    if transformer_apis:
        with dot.subgraph(name='cluster_transformers') as transformers:
            transformers.attr(label='Processors', fontsize='12', style='bold')
            transformers.attr(color='blue', style='rounded')
            
            for api in transformer_apis:
                display_name = format_api_name(api)
                transformers.node(api, display_name, fillcolor='lightblue')
    
    # Add consumer APIs
    if consumer_apis:
        with dot.subgraph(name='cluster_consumers') as consumers:
            consumers.attr(label='Data Consumers', fontsize='12', style='bold')
            consumers.attr(color='red', style='rounded')
            
            for api in consumer_apis:
                display_name = format_api_name(api)
                consumers.node(api, display_name, fillcolor='lightcoral')

def generate_svg_safely(dot, filename):
    """Generate SVG with multiple fallback methods"""
    try:
        # Method 1: Direct render
        dot.format = 'svg'
        dot.render(filename, cleanup=True)
        print(f"✓ Generated {filename}.svg using direct render")
        return True
    except Exception as e:
        print(f"Direct render failed: {e}")
        
        try:
            # Method 2: Pipe method
            svg_content = dot.pipe(format='svg', encoding='utf-8')
            with open(f'{filename}.svg', 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✓ Generated {filename}.svg using pipe method")
            return True
        except Exception as e2:
            print(f"Pipe method failed: {e2}")
            
            try:
                # Method 3: Source method with external call
                dot_source = dot.source
                with open(f'{filename}.dot', 'w') as f:
                    f.write(dot_source)
                print(f"✓ Generated {filename}.dot - you can manually convert to SVG")
                print(f"  Run: dot -Tsvg {filename}.dot -o {filename}.svg")
                return False
            except Exception as e3:
                print(f"All methods failed: {e3}")
                return False

def main():
    # Load the API data
    try:
        with open("interface_1.json") as f:
            api_data = json.load(f)
    except FileNotFoundError:
        print("Error: interface_1.json not found!")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    print("Creating improved Graphviz API connection diagrams...")
    
    # Create the standard simplified view
    print("Creating simple connection view...")
    dot_simple = create_graphviz_api_graph(api_data, "api_connections_simple")
    
    # Create hierarchical view
    print("Creating hierarchical view...")
    dot_hierarchy = create_hierarchical_layout(api_data, "api_hierarchy")
    
    # Generate SVG files with improved error handling
    print("\nGenerating SVG files...")
    
    simple_success = generate_svg_safely(dot_simple, 'api_connections_simple')
    hierarchy_success = generate_svg_safely(dot_hierarchy, 'api_hierarchy')
    
    # Always save DOT source files
    try:
        with open('api_connections_simple.dot', 'w') as f:
            f.write(dot_simple.source)
        print("✓ Generated api_connections_simple.dot")
        
        with open('api_hierarchy.dot', 'w') as f:
            f.write(dot_hierarchy.source)
        print("✓ Generated api_hierarchy.dot")
    except Exception as e:
        print(f"Error saving DOT files: {e}")
    
    # Print summary
    print(f"\nGeneration Summary:")
    print(f"- Simple view SVG: {'✓' if simple_success else '✗'}")
    print(f"- Hierarchy view SVG: {'✓' if hierarchy_success else '✗'}")
    print(f"- DOT source files: ✓")
    
    # Print statistics
    api_count = len(api_data["APIs"])
    edge_count = len(api_data.get("edges", []))
    print(f"\nDiagram Statistics:")
    print(f"- {api_count} APIs")
    print(f"- {edge_count} connections")
    
    if not (simple_success and hierarchy_success):
        print(f"\nTroubleshooting:")
        print(f"- Ensure Graphviz is installed: pip install graphviz")
        print(f"- Check if 'dot' command is in your PATH")
        print(f"- You can manually convert DOT files using: dot -Tsvg filename.dot -o filename.svg")

if __name__ == "__main__":
    main()
