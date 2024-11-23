import networkx as nx
import matplotlib.pyplot as plt

draw = True

#G = nx.DiGraph()
G = nx.scale_free_graph(100, seed = 4)

print("Weakly Connected?")
print(nx.is_weakly_connected(G))

#print(G.edges())

#print("G")
if draw:
    nx.draw_networkx(G, arrows = True)
    plt.show()

# Reduce G to its strongly connected components, with the nodes of the components being represented by a representative of G
C = nx.condensation(G)

# Since the nodes of C are relabelled, whenever we add an edge, it actually needs to be using the mapping of the nodes in C to nodes in G.
#print(C.nodes[0]['members'])
representatives = [list(C.nodes[i]['members'])[0] for i in range(len(C))]

print(representatives)

if draw:
    nx.draw_networkx(C, arrows = True)
    plt.show()

vision = dict()  # the dictionary of sinks each source points at
sinks = set() # The set of sinks
sources = set() # The set of source


# Find the set of sinks, and sources
for node in C:
    if C.in_degree(node) == 0: # A source if in degree is zero
        sources.add(node)
    if C.out_degree(node) == 0: # A sink if out degree is zero
        sinks.add(node)


# This is calculating the visions of each source
vision = dict()
for source in sources:
    descendants = nx.descendants(C, source)
    vision[source] = set.intersection(set(descendants),sinks)

print(sources)
print(sinks)
print(vision)

### given directed bi graph of sources and sinks, represented by sources, sinks and dictionary of successors of sources


m= len(sinks)
n = len(sources)

edges_to_add = list()
visible_sinks = set()
connected_sinks = set()
connected_sources = set()

first_source = list(sources)[0]
visible_sinks = set(vision[first_source])

# first make it so our first source can 'see' all sinks
while visible_sinks != sinks:
    for source in set.difference(sources, connected_sources):
        # Find any possible sinks our selected source can't see yet
        possible_sinks_to_add = list(set.intersection(set.difference(sinks, set(visible_sinks)), set(vision[source])))

        #If there is a sink we haven't added that can be seen by the source we chose, but not the original source, add it.
        if len(possible_sinks_to_add) != 0:
            sink_to_add = list(set.difference(visible_sinks, connected_sinks))[0] # We connect an unconnected sink in the visible sinks, to the source we chose.
            connected_sinks.add(sink_to_add) # the sink is now connected, and no longer a sink
            edges_to_add.append((representatives[sink_to_add], representatives[source])) # We record the edge we add to our original graph
            visible_sinks = set.union(visible_sinks, set(possible_sinks_to_add)) # We update the list of visible sinks
            connected_sources.add(source) # the source is now connected, and no longer a source
            break



# now replace first source repeatedly until all sinks or all sources except one are connected

while len(connected_sinks) < m -1 and len(connected_sources) < n - 1:
    for source in set.difference(set.difference(sources, set([first_source])), connected_sources):
        possible_sinks_to_add = list(set.difference(sinks, connected_sinks)) # we for each source, we essentially make it the source that can see everything until there are no sinks

        if len(possible_sinks_to_add) != 0: # This check is actually unnecessary given the requirements above
            connected_sinks.add(possible_sinks_to_add[0]) # We connect the sink identified
            connected_sources.add(first_source) # Connect the first source
            edges_to_add.append((representatives[possible_sinks_to_add[0]], representatives[first_source])) # Add the edge between the sink and the first source
            first_source = source # Replace the first source, so we can apply the same algorithm again

# we are now in the state where either all sources or all sinks are connected, so we just connect the remainder

# in any case we connect the 1 to all the others

for source in set.difference(sources, connected_sources):
    edges_to_add.append((representatives[list(sinks)[0]], representatives[source]))

for sink in set.difference(sinks, connected_sinks):
    edges_to_add.append((representatives[sink], representatives[list(sources)[0]]))
    

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


if draw:
    nx.draw_networkx(P, arrows = True)
    plt.show()
print("Strongly Connected?")
print(nx.is_strongly_connected(P))