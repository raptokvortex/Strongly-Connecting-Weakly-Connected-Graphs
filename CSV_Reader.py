import networkx as nx
from Connectors import strong_connector

# Read the edge list with weights

# G = nx.read_edgelist(
#     'bio-CE-CX.edges',
#     create_using=nx.DiGraph(),
#     delimiter=' ',
#     data=(('weight', float),)  # Specify that the third column is a weight (float)
# )


# def graph_reader(edgelist):
#     G = nx.read_edgelist(
#         edgelist,
#         create_using=nx.DiGraph(),
#         delimiter=' ',
#         data=(('weight', float),)  # Specify that the third column is a weight (float)
#     )
#     return G
# G = G.reverse()
# G = nx.DiGraph()

# G.add_nodes_from([1,2,3,4,5,6,7,8,9])


# G.add_edges_from([(1,2),(2,3),(3,1),(4,5),(5,6),(6,4),(7,8),(8,9), (9,7), (2,4), (2,7)])

G = nx.scale_free_graph(20, seed = 0)

P = strong_connector(G, how_to_find_condensations = 0, how_to_find_visions = 2, draw = True, debug = True, final_readout= True, weakly_connected_check = True)

# print(nx.is_strongly_connected(P))

