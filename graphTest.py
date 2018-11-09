import networkx as nx

G = nx.Graph()
G = nx.read_gml('test.gml')

G.add_node(2)

nx.write_gml(G, 'test.gml')
