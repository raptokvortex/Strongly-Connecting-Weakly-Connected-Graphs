import networkx as nx
from Visions import vision_finder2


def fast_step_1(C):
    # Find the vision of the sources
    sources, sinks, source_visions = vision_finder2(C)
    # Find which sinks are reached by certain sources
    sinks, sources, sink_pre_visions = vision_finder2(C.reverse())


    # We want to record the list of sources that covers the set
    sink_covering = []

    # And we record the the sinks that we identified that mapped to the sources
    unique_sinks = []

    # We generate a list with length of the number of sinks, to record each sink that is visible (0 for not visible, 1 if visible)
    visible_sinks = [0 for i in range(len(sinks))]

    
    sink_indexes = dict()
    i = 0
    for sink in sinks:
        sink_indexes[sink] = i
        i += 1

    
    # We have to check for each sink, (m sinks), then update the sinks for each sink the source could see (possibly m)
    for i in range(len(sinks)):
        if visible_sinks[i] == 0: # If we cannot see a sink yet
            unique_sinks.append(sinks[i]) # We add our sink to the list of sinks we are going to connect
            source_to_add = sink_pre_visions[sinks[i]][0] # And find a source that can see it
            sink_covering.append(source_to_add) # Add the source that can see it
            for sink in source_visions[source_to_add]: # From the source, update the sinks in the visible sinks links so that we can see them
                visible_sinks[sink_indexes[sink]] = 1

    return sources, sinks, source_visions, sink_pre_visions, sink_covering, unique_sinks
