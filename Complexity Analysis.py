import networkx as nx
from Connectors import strong_connector
from Connectors_Version_2 import fast_strong_connector
#from CSV_Reader import graph_reader
import matplotlib.pyplot as plt
import time

twitter = nx.read_edgelist("twitter_combined.txt", create_using=nx.DiGraph(), nodetype=int)
print("Read Twitter")

wikispeed = nx.read_edgelist("links.tsv", create_using = nx.DiGraph(), nodetype=str)
print("Read wikispeed")

wikivote = nx.read_edgelist("Wiki-Vote.txt", create_using = nx.DiGraph(), nodetype=int)
print("Read wikivote")

congressnet = nx.read_edgelist("congress.edgelist", create_using=nx.DiGraph(), nodetype=int)
print("Read congressnet")

gnutella = nx.read_edgelist("p2p-Gnutella08.txt", create_using=nx.DiGraph(), nodetype=int)
print("Read gnutella")

scale_free_1 = nx.scale_free_graph(100)
print("Generated Scale Free Graph 1")

scale_free_2 = nx.scale_free_graph(1000)
print("Generated Scale Free Graph 2")

scale_free_3 = nx.scale_free_graph(3000)
print("Generated Scale Free Graph 3")

scale_free_4 = nx.scale_free_graph(6000)
print("Generated Scale Free Graph 4")

scale_free_5 = nx.scale_free_graph(12000)
print("Generated Scale Free Graph 5")

scale_free_6 = nx.scale_free_graph(30000)
print("Generated Scale Free Graph 6")

scale_free_7 = nx.scale_free_graph(50000)
print("Generated Scale Free Graph 7")

gnc_1 = nx.gnc_graph(100)
print("Generated Scale GNC Graph 1")

gnc_2 = nx.gnc_graph(1000)
print("Generated Scale GNC Graph 2")

gnc_3 = nx.gnc_graph(10000)
print("Generated Scale GNC Graph 3")

gnc_4 = nx.gnc_graph(50000)
print("Generated Scale GNC Graph 4")

gnc_5 = nx.gnc_graph(100000)
print("Generated Scale GNC Graph 5")

scale_free_graphs = [scale_free_1, scale_free_2, scale_free_3, scale_free_4, scale_free_5, scale_free_6, scale_free_7]

gnc_graphs = [gnc_1, gnc_2, gnc_3, gnc_4, gnc_5]

real_graphs = [twitter, wikispeed, wikivote, congressnet, gnutella]

edges = []
vertices = []
verticesandedges = []
times = []
sources = []
sinks = []
sourceandsinks = []

# basically spends its whole time in step 1

for graph in scale_free_graphs + gnc_graphs + real_graphs:
    edges.append(len(graph.edges))
    print("Edges")
    print(edges[-1])
    vertices.append(len(graph.nodes))
    print("Vertices")
    print(vertices[-1])
    verticesandedges.append(edges[-1] + vertices[-1])
    start = time.time()
    # P, m, n =strong_connector(graph, how_to_find_condensations = 0, how_to_find_visions = 2, debug = True)
    P, m, n =fast_strong_connector(graph, final_readout = True)
    end = time.time()
    times.append(end - start)
    sources.append(n)
    sinks.append(m)
    sourceandsinks.append(m + n)
    print("Time")
    print(times[-1])

plt.scatter(verticesandedges, times)
plt.show()

plt.scatter(edges, times)
plt.show()

plt.scatter(vertices, times)
plt.show()

plt.scatter(sources, times)
plt.show()

plt.scatter(sinks, times)
plt.show()

# This appears to show the bottleneck the best, which makes sense, since I wrote my code with a lot of set functions which are expensive
plt.scatter(sourceandsinks, times)
plt.show()




