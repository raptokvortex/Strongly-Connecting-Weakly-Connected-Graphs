import networkx as nx
from Connectors import strong_connector

scale_free_4 = nx.scale_free_graph(40000)
print("Generated Scale Free Graph 4")

scale_free_5 = nx.scale_free_graph(100000)
print("Generated Scale Free Graph 5")

strong_connector(scale_free_4, how_to_find_condensations = 0, how_to_find_visions = 2, final_readout = True)