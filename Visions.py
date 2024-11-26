# Given a directed acylcic graph, want to return sources, sinks, and visions of the sources

import networkx as nx

class vertex:
    def __init__(self, rep, indegree, outdegree):
        self.rep = rep # representative
        self.indegree = indegree 
        self.outdegree = outdegree 
        self.backprops = 0 # number of times a vertex has been backpropogated to
        self.vision = set() # the current elements the vertex can see
        pass

    def __str__(self):
        return f"{self.rep}"
    

def vision_finder(G):
    """For G an acylcic graph, returns a list of sources, a list of sinks, and a dictionary of sources with entries being their visions. 
    (The sinks where there is a path from that source to the sink)"""

    true_sinks = [] # want a list of the true sinks, which we will return
    current_sinks = [] # want a list of the items we are treating as current sinks for each step of the algorithm
    true_sources = []  # want a list of true sources, which we will return
    vertices = {} # creating a dictionary of the vertices with our vertex class, which have our desired properties
    
    for node in G:
        vertices[node] = vertex(node, G.in_degree(node), G.out_degree(node))
        if G.in_degree(node) == 0:
            true_sources.append(node)
        if G.out_degree(node) == 0:
            true_sinks.append(node)
            current_sinks.append(vertices[node])
            vertices[node].vision.add(node) # If the vertex is a sink, it can certainly see itself
    
    sinklength = len(true_sinks)
    while sinklength != 0: # We want to terminate when we have no more back propagations to do
        new_sinks = set()
        for vrtx in current_sinks:
            
            predecessors = G.predecessors(vrtx.rep) # This just asks what vertices point to our vertex. There's no algorithm behind this, and so we won't reproduce it from scratch.
            
            if True: # len(list(predecessors)) > 0: # Can only back propagate if the vertex has predecessors (i.e. is not a source)
                for predecessor in predecessors:
                    vertices[predecessor].backprops += 1 # we record the number of times we back propogate
                    vertices[predecessor].vision = set.union(vertices[predecessor].vision ,vrtx.vision) # We add the vision of any vertices we can reach
                    if vertices[predecessor].backprops == vertices[predecessor].outdegree: # for the next step we treat the vertex as a sink, like in the previous step
                        new_sinks.add(vertices[predecessor])
        sinklength = len(new_sinks)

        current_sinks = list(new_sinks)

    # Now we know that each vertex is lableled with its vision, so we just return the final labels 
    # Note: this algorithm could easily be modified to return the successors of every vertex, rather than just the visions of the sources
    visions = dict()
    for source in true_sources:
        visions[source] = vertices[source].vision

    return set(true_sources), set(true_sinks), visions
    
# ######################################################################################
# # Testing new algorithm

# G = nx.scale_free_graph(100, seed = 2)

# # Reduce G to its strongly connected components, with the nodes of the components being represented by a representative of G
# C = nx.condensation(G)

# vision = dict()  # the dictionary of sinks each source points at
# sinks = set() # The set of sinks
# sources = set() # The set of source


# # Find the set of sinks, and sources
# for node in C:
#     if C.in_degree(node) == 0: # A source if in degree is zero
#         sources.add(node)
#     if C.out_degree(node) == 0: # A sink if out degree is zero
#         sinks.add(node)


# # This is calculating the visions of each source
# vision = dict()
# for source in sources:
#     descendants = nx.descendants(C, source)
#     vision[source] = set.intersection(set(descendants),sinks)

# new_sources, new_sinks, new_vision = vision_finder(C)

# print("Original: Sources")
# print(sources)
# print("New algorithm: Sources")
# print(set(new_sources))

# print("*************************************************")
# print("Original: Sinks")
# print(sinks)
# print("New algorithm: Sinks")
# print(set(new_sinks))

# print("*************************************************")
# print("Original: Vision")
# print(vision)
# print("New algorithm: Vision")
# print(new_vision)

# print(vision == new_vision)




        