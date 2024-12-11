# This is just a function implementation of our algorithm to strongly connect a graph
import networkx as nx
import matplotlib.pyplot as plt
import Condensations
from faststep1 import fast_step_1

def fast_strong_connector(G, how_to_find_condensations = 0, disconnected_possibility = False, final_readout = False, draw = False, debug = False, weakly_connected_check = False ):
    """
    Take a directed networkx graph G, and returns a graph with a minimal number of edges added in order to strongly connect it. Does step 1 of the algorithm in a fast way, but relies on our method for finding visions in order to do so
    G - a networkx DiGraph object, representing a directed graph. If disconnected ensure disconnected possibility is True, and that how_to_find_visions = 2
    how_to_find_visions = 2 # 2 - Use our BFS based algorithm for finding visions only (Should be O(V+E), as only checks each vertex and edge once, and so is optimal in some sense)
    how_to_find_condensations = 1 # 0 Use networkxx implementation of condensation (Should be O(V+E), using an appropriate algorithm)
                                  # 1 Use our implementation to find a condensation (We think this may be as bad as O(V**2)). Specifically O(V(V+E))
    disconnected_possibility = True # If the graph was disconnected, the way the algorithm is currently implemented, we could possibly add a spurious edge of a node to itself. Set this to true to remove the edge
    final_readout = False # If we want the final read out of the number of edges we added, the number of sources and sinks in the condensation, and whether we indeed did strongly connect the graph (using networkx method)
    draw = False # If we want to draw the Graph, Condensation, and Augmented graph
    debug = False # Outputs some intermediate steps if True, like visions, sources etc
    weakly_connected_check = False # Check if the graph was weakly connected in the first place, and prints out if it was
    """
    # Weakly Connected Check
    if weakly_connected_check:
        print("Weakly Connected?")
        print(nx.is_weakly_connected(G))

    # Draw the initial graph for debugging
    if draw:
        nx.draw_networkx(G, arrows = True)
        plt.title('G')
        plt.show()

    # networkx method to find condensation
    if how_to_find_condensations == 0:
        # Reduce G to its strongly connected components, with the nodes of the components being represented by a representative of G
        C = nx.condensation(G)

        # Since the nodes of C are relabelled, whenever we add an edge, it actually needs to be using the mapping of the nodes in C to nodes in G.
        representatives = [list(C.nodes[i]['members'])[0] for i in range(len(C))]


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

    # Show the condenseded intermediate step if draw is True
    if draw:
        nx.draw_networkx(C, arrows = True)
        plt.title('Condensed Graph')
        plt.show()

    ##########################################################
    # STEP 1
    ##########################################################

    # Use fast_step_1 algorithm, to compute sources, sinks, sink_cover, unique_sinks and visions of sources etc
    sources, sinks, source_vision, sink_pre_vision, sink_cover, unique_sinks = fast_step_1(C)

    # Set to sets so that we can do intersections etc
    sources = set(sources)
    sinks = set(sinks)

    if debug:
        print("************************")
        print("Sources:")
        print(sources)
        print("************************")
        print("Sinks:")
        print(sinks)
        print("************************")
        print("Vision:")
        print(source_vision)
        print("************************")


    # Do the main body of step 1 adding our edges to the list of edges we're going to add to the original graph.
    m = len(sinks)
    n = len(sources)

    edges_to_add = list()
    connected_sinks = set()
    connected_sources = set()

    # Identify the sources which we will make see everything
    first_source = sink_cover[0]

    # Since we known that our list of sources and sinks computed in fast step 1 is already appropriate by construciton, we just add the relevant edges
    for i in range(1, len(sink_cover)):
        if debug:
            print("Step 1 Occurred")
        connected_sources.add(sink_cover[i])
        connected_sinks.add(unique_sinks[i-1])
        edges_to_add.append((representatives[unique_sinks[i-1]], representatives[sink_cover[i]])) # Add the edge between the sink and the first source

    ##############################################
    # Step 2
    ##############################################

    # now replace first source repeatedly until all sinks or all sources except one are connected

    while len(connected_sinks) < m -1 and len(connected_sources) < n - 1:
        if debug:
            print("Step 2 Occurred")
        for source in set.difference(set.difference(sources, set([first_source])), connected_sources):
            possible_sinks_to_add = list(set.difference(sinks, connected_sinks)) #for each source, we essentially make it the source that can see everything until there are no sinks

            if len(possible_sinks_to_add) != 0 and len(connected_sinks) != m-1: # If there's only 1 sink to add
                connected_sinks.add(possible_sinks_to_add[0]) # We connect the sink identified
                connected_sources.add(first_source) # Connect the first source
                edges_to_add.append((representatives[possible_sinks_to_add[0]], representatives[first_source])) # Add the edge between the sink and the first source
                first_source = source # Replace the first source, so we can apply the same algorithm again

    
    ############################################
    # Step 3
    ############################################
    # we are now in the state where either all sources or all sinks are connected, so we just connect the remainder

    # in either case we connect the 1 to all the others

    remaining_sources = list(set.difference(sources, connected_sources))
    remaining_sinks = list(set.difference(sinks, connected_sinks))

    if debug:
        print("remaining sources")
        print(remaining_sources)

        print("remaining sinks")
        print(remaining_sinks)
    
    if len(remaining_sinks) == 1:
        for source in remaining_sources:
            edges_to_add.append((representatives[remaining_sinks[0]], representatives[source]))
            if debug:
                print("I added the following edge in step 3")
                print(edges_to_add[-1])

    else:
        for sink in remaining_sinks:
            edges_to_add.append((representatives[sink], representatives[remaining_sources[0]]))
            if debug:
                print("I added the following edge in step 3")
                print(edges_to_add[-1])
        
    # If the graph was disconnected, we could possibly add an edge to itself, and so we remove it
    if disconnected_possibility:
        edges_to_remove = []
        for edge in edges_to_add:
            if edge[0] == edge[1]:
                edges_to_remove.append(edge)
        
        for edge in edges_to_remove:
            edges_to_add.remove(edge)

    # Create a new graph, from a copy of the original, and add the edges we found to it
    edges_required = len(edges_to_add)
    P = G.copy()
    P.add_edges_from(edges_to_add)


    if debug:
        print("Added edges:")
        print(edges_to_add)

        print("Condensation's Sources")
        print(n)
        print("Condensation's Sinks")
        print(m)
        print("Edges Required")
        print(edges_required)


    if draw:
        nx.draw_networkx(P, arrows = True)
        plt.title("Augmented Graph")
        plt.show()

    if debug:
        print("Added edges:")
        print(edges_to_add)

    # Read out the final results of the algorithm with some key statistics
    if final_readout:
        print("Condensation's Sources")
        print(n)
        print("Condensation's Sinks")
        print(m)
        print("Edges Required")
        print(edges_required)
        print("Strongly Connected?")
        print(nx.is_strongly_connected(P))

    return P, m, n

