import networkx as nx
import matplotlib.pyplot as plt

#G = nx.DiGraph()

#G = nx.gn_graph(20)

G = nx.scale_free_graph(10, seed = 0)

if not nx.is_weakly_connected(G):
    quit()

#print(G.edges())

#print("G")
nx.draw_networkx(G, arrows = True)
plt.show()

# Reduce G to its strongly connected components, with the nodes of the components being represented by a representative of G
C = nx.condensation(G)

# Since the nodes of C are relabelled, whenever we add an edge, it actually needs to be using the mapping of the nodes in C to nodes in G.
print(C.nodes[0]['members'])
representatives = [list(C.nodes[i]['members'])[0] for i in range(len(C))]
print(representatives)

nx.draw_networkx(C, arrows = True)
plt.show()

#print(C.edges())

#print("Condensation of G")
#nx.draw(C)

source_sink_image = dict()  # the dictionary of sinks each source points at
sinks = set()
sources = set()



for node in C:
    if C.in_degree(node) == 0:
        sources.add(node)
    if C.out_degree(node) == 0:
        sinks.add(node)

# this is not quite working properly
# it's not returning the full list of verticies that each source can see
source_sink_image = dict()
for source in sources:
    descendants = nx.descendants(C, source)
    source_sink_image[source] = set.intersection(set(descendants),sinks)

print(sources)
print(sinks)
print(source_sink_image)

### given directed bi graph of sources and sinks, represented by sources, sinks and dictionary of successors of sources


m= len(sinks)
n = len(sources)

edges_to_add = list()
visible_sinks = set()
connected_sinks = set()
connected_sources = set()

first_source = list(sources)[0]
visible_sinks = set(source_sink_image[first_source])

# first make it so our first source can 'see' all sinks
while visible_sinks != sinks:
    for source in set.difference(sources, connected_sources):
        possible_sinks_to_add = list(set.intersection(set.difference(sinks, visible_sinks), set(source_sink_image[source])))

        if len(possible_sinks_to_add) != 0:
            visible_sinks = set.union(visible_sinks, set(possible_sinks_to_add))
            connected_sinks.add(possible_sinks_to_add[0])
            connected_sources.add(source)
            edges_to_add.append((representatives[possible_sinks_to_add[0]], representatives[source]))
            break

# now replace first source repeatedly until all sinks or all sources are connected

while len(connected_sinks) < m -1 and len(connected_sources) < n - 1:
    for source in set.difference(sources, connected_sources):
        possible_sinks_to_add = list(set.intersection(set.difference(sinks, connected_sinks), set(source_sink_image[source])))

        if len(possible_sinks_to_add) != 0:
            connected_sinks.add(possible_sinks_to_add[0])
            connected_sources.add(first_source)
            edges_to_add.append((representatives[possible_sinks_to_add[0]], representatives[first_source]))
            first_source = source

# we are now potentially left with 1 source and 1 sink, 1 source and k sinks, or k sources and 1 sink

# in any case we connect the 1 to all the others

for source in set.difference(sources, connected_sources):
    for sink in set.difference(sinks, connected_sinks):
        edges_to_add.append((representatives[sink], representatives[source]))

connected_sinks = sinks
connected_sources = sources

edges_required = len(edges_to_add)

P = G.copy()
#print(edges_to_add)
P.add_edges_from(edges_to_add)

print("Added edges:")
print(edges_to_add)

print("Sources")
print(n)
print("Sinks")
print(m)
print("Edges Required")
print(edges_required)

#print("Final Graph")

#nx.draw(P)

#nx.write_gexf(G, "weak.gexf")

#nx.write_gexf(C, "condensed.gexf")
#nx.write_gexf(P, "augmented.gexf")
nx.draw_networkx(P, arrows = True)
plt.show()
print(nx.is_strongly_connected(P))
