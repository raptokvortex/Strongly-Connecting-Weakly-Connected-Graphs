# This is just a function implementation of our algorithm to strongly connect a graph
import networkx as nx
import matplotlib.pyplot as plt
import Visions
import Condensations

def strong_connector(G, how_to_find_visions = 2, how_to_find_condensations = 0, disconnected_possibility = False, final_readout = False, draw = False, debug = False, weakly_connected_check = False ):
    """
    Take a directed networkx graph G, and returns a graph with a minimal number of edges added in order to strongly connect it.
    G - a networkx DiGraph object, representing a directed graph. If disconnected ensure disconnected possibility is True, and that how_to_find_visions = 2
    how_to_find_visions = 2 # 0 - Use networkx implementation of descendants # Must be set to 2 if the graph is disconnected
                            # 1 - Use our DFS (depth first search) based implementation of descendants (inefficient, as we have to cover some vertices and edges twice when looking at each source) # Must be set to 2 if the graph is disconnected
                            # 2 - Use our DFS based algorithm for finding visions only (Should be O(V+E), as only checks each vertex and edge once, and so is optimal in some sense)
    how_to_find_condensations = 1 # 0 Use networkxx implementation of condensation (Should be O(V+E), using an appropriate algorithm)
                                  # 1 Use our implementation to find a condensation (We think this may be as bad as O(V**2)). Specifically O(V(V+E))
    disconnected_possibility = True # If the graph was disconnected, the way the algorithm is currently implemented, we could possibly add a spurious edge of a node to itself. Set this to true to remove the edge
    final_readout = False # If we want the final read out of the number of edges we added, the number of sources and sinks in the condensation, and whether we indeed did strongly connect the graph (using networkx method)
    draw = False # If we want to draw the Graph, Condensation, and Augmented graph
    debug = False # Outputs some intermediate steps if True, like visions, sources etc
    weakly_connected_check = False # Check if the graph was weakly connected in the first place, and prints out if it was
    """


    if weakly_connected_check:
        print("Weakly Connected?")
        print(nx.is_weakly_connected(G))

    #print("G")
    if draw:
        nx.draw_networkx(G, arrows = True)
        plt.show()

    # networkx method to find condensation
    if how_to_find_condensations == 0:
        # Reduce G to its strongly connected components, with the nodes of the components being represented by a representative of G
        C = nx.condensation(G)

        # Since the nodes of C are relabelled, whenever we add an edge, it actually needs to be using the mapping of the nodes in C to nodes in G.
        #print(C.nodes[0]['members'])
        representatives = [list(C.nodes[i]['members'])[0] for i in range(len(C))]

        # print(representatives)

    # our method to find condensation
    elif how_to_find_condensations == 1:
        C = Condensations.condensation(G)

        # Since we labelled our nodes in a sensible way already, we make a list with each entry its own label
        representatives = [i for i in range(0,len(G))]

    else:
        print("Selection of condensation method incorrect. Please choose 0, 1")

    # A quick to check if the graph was strongly connected. If it was we are left with a single node
    if len(C) == 1:
        if final_readout:
            print("Graph is already strongly connected, and therefore no edges were added")
        return G

    if draw:
        nx.draw_networkx(C, arrows = True)
        plt.show()

    # Using networkx implementation
    if how_to_find_visions == 0:
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

    # Using a dfs based implementation to find descendants
    elif how_to_find_visions == 1:
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
            descendants = Condensations.find_descendants(C, source)
            vision[source] = set.intersection(set(descendants),sinks)

    # Using our own implementation to efficiently find visions
    elif how_to_find_visions == 2:
        sources, sinks, vision = Visions.vision_finder(C)

    else:
        print("Selection of vision method incorrect. Please choose 0, 1 or 2")

    if debug:
        print("************************")
        print("Sources:")
        print(sources)
        print("************************")
        print("Sinks:")
        print(sinks)
        print("************************")
        print("Vision:")
        print(vision)
        print("************************")

    ### given directed bi graph of sources and sinks, represented by sources, sinks and dictionary of successors of sources


    m = len(sinks)
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

    # in either case we connect the 1 to all the others

    for source in set.difference(sources, connected_sources):
        edges_to_add.append((representatives[list(sinks)[0]], representatives[source]))

    for sink in set.difference(sinks, connected_sinks):
        edges_to_add.append((representatives[sink], representatives[list(sources)[0]]))
        

    if disconnected_possibility:
        edges_to_remove = []
        for edge in edges_to_add:
            if edge[0] == edge[1]:
                edges_to_remove.append(edge)
        
        for edge in edges_to_remove:
            edges_to_add.remove(edge)

    edges_required = len(edges_to_add)

    P = G.copy()
    #print(edges_to_add)
    P.add_edges_from(edges_to_add)


    if debug:
        print("Added edges:")
        print(edges_to_add)

        print("Condensation's Sources")
        print(n)
        print("Condenssation's Sinks")
        print(m)
        print("Edges Required")
        print(edges_required)


    if draw:
        nx.draw_networkx(P, arrows = True)
        plt.show()

    if debug:
        print("Added edges:")
        print(edges_to_add)

    if final_readout:
        print("Condensation's Sources")
        print(n)
        print("Condenssation's Sinks")
        print(m)
        print("Edges Required")
        print(edges_required)
        print("Strongly Connected?")
        print(nx.is_strongly_connected(P))
    
    return P

