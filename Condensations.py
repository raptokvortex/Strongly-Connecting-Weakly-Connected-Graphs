import networkx as nx

def find_descendants(graph, start_node):
    
    descendants = set()

    def dfs(node):
        for neighbor in graph[node]:  # Iterate through all neighbors of the current node
            if neighbor not in descendants:  # If the neighbor has not been visited
                descendants.add(neighbor)  # Mark it as visited
                dfs(neighbor)  # Recursively visit this neighbor

    dfs(start_node)
    return descendants

def condensation(G):
    """
    Takes a directed, weakly connected graph G, and returns the condensation of the graph P
    """
    dic = dict()
    for i in G.nodes:
        dic[i] = find_descendants(G, i)

    from collections import defaultdict

    dic2 = defaultdict(set)
    visited = set()  # Used to mark all processed nodes

    for i in dic.keys():
        if i in visited:
            continue  # Skip if the current node has already been processed
        # Current node is not processed; create a new strongly connected component
        for j in dic[i]:
            if i in dic[j]:  # Strongly connected component
                dic2[i].add(j)
                dic2[i].add(i)  # Add itself to the strongly connected component
                visited.update(dic2[i])  # Mark all nodes in this component as processed

        # If i has not been marked, add itself as an individual weakly connected component
        if i not in visited:
            dic2[i].add(i)
            visited.add(i)

    # Want to make a condensed graph
    P = nx.DiGraph()

    P.add_nodes_from(list(dic2.keys()))

    representatives = dict()
    for node in dic2.keys():
        for component_item in dic2[node]:
            representatives[component_item] = node

    edges_to_add = set()
    for edge in G.edges:
        if representatives[edge[0]] != representatives[edge[1]]:
            edges_to_add.add(((representatives[edge[0]]), representatives[edge[1]]))

    edges_to_add = list(edges_to_add)

    P.add_edges_from(edges_to_add)

    return P
