import graphviz

# Create a directed graph
dot = graphviz.Digraph(comment='My Simple Graph')

# Add nodes
dot.node('Avv', 'Node A Label', id='A', color='red')
dot.node('A', 'Node B Label', id='node_b')
dot.node('B', 'Node B Label')
dot.node('C', 'Node C Label')

# Add edges
dot.edge('Avv', 'B', 'Edge AB')
dot.edge('B', 'C', 'Edge BC')
dot.edge('C', 'A', 'Edge CA')

# Render the graph to a PDF file and open it
# print(dir(dot))
dot.render('simple_graph', format='svg')
