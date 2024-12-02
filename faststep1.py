import networkx as nx
from Visions import vision_finder2


def fast_step_1(C):
    sources, sinks, source_visions = vision_finder2(C)
    sinks, sources, sink_pre_visions = vision_finder2(C.reverse())

    sink_covering = []
    visible_sinks = [0 for i in range(len(sinks))]
    sink_indexes = dict()
    i = 0
    for sink in sinks:
        sink_indexes[sink] = i
        i += 1

    unique_sinks = []
    # We have to check for each sink, (m sinks), then update the sinks for each sink the source could see (possibly m)
    for i in range(len(sinks)):
        if visible_sinks[i] == 0: # If we cannot see a sink yet
            unique_sinks.append(sinks[i])
            source_to_add = sink_pre_visions[sinks[i]][0]
            sink_covering.append(source_to_add) # Add the first source
            for sink in source_visions[source_to_add]: # From the first source, update the sinks in the visible sinks so that we can see them
                visible_sinks[sink_indexes[sink]] = 1

    return sources, sinks, source_visions, sink_pre_visions, sink_covering, unique_sinks

# sources, sinks, source_visions, sink_pre_visions, sink_covering, unique_sinks = fast_step_1(C)


# G = nx.scale_free_graph(100)

# C = nx.condensation(G)


# print(sources)
# print(sinks)
# for source in sink_covering:
#     print(source, source_visions[source])