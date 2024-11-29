import networkx as nx
from Connectors import strong_connector

# Read the edge list with weights
G = nx.read_edgelist(
    'bio-CE-CX.edges',
    create_using=nx.DiGraph(),
    delimiter=' ',
    data=(('weight', float),)  # Specify that the third column is a weight (float)
)

# G = G.reverse()
# G = nx.DiGraph()

# G.add_nodes_from([1,2,3,4,5,6,7,8,9])


# G.add_edges_from([(1,2),(2,3),(3,1),(4,5),(5,6),(6,4),(7,8),(8,9), (9,7), (2,4), (2,7)])

P, required_edges, representatives = strong_connector(G, final_readout = True, weakly_connected_check = True, disconnected_possibility = True, debug = True)

list_of_sinks = []
repeat_edges = []
for edge in required_edges:
    if edge[0] in list_of_sinks:
        print(edge[0])
        for new_edge in required_edges:
            if edge[0] == new_edge[0]:
                repeat_edges.append(new_edge)
        break        
    list_of_sinks.append(edge[0])
    

for i in range(len(representatives)):
    if representatives[i] == repeat_edges[0][0]:
        print(i)

print(repeat_edges)

P.remove_edge(repeat_edges[0][0], repeat_edges[0][1])
print("Edge 1 to be removed")
print(repeat_edges[0])
print("Strongly Connected after removing:")
print(nx.is_strongly_connected(P))

P.add_edge(repeat_edges[0][0], repeat_edges[0][1])
P.remove_edge(repeat_edges[1][0], repeat_edges[1][1])
print("Edge 2 to be removed")
print(repeat_edges[1])
print("Strongly Connected after removing:")
print(nx.is_strongly_connected(P))