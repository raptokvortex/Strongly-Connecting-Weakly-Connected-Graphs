# Condensed 

import networkx as nx

def find_descendants(graph, start_node):
    
    descendants = set()

    def dfs(node):
        for neighbor in graph[node]:  # 遍历当前节点的所有邻居
            if neighbor not in descendants:  # 如果该邻居尚未访问
                descendants.add(neighbor)  # 标记为访问过
                dfs(neighbor)  # 递归访问该邻居

    dfs(start_node)
    return descendants

def condensation(G):
    """
    Takes a directed, weakly connected graph G, and returns the condensation of the graph P
    """
    dic = dict()
    for i in G.nodes:
        dic[i] = find_descendants(G,i)


    from collections import defaultdict

    dic2 = defaultdict(set)
    visited = set()  # 用于标记所有已处理的节点

    for i in dic.keys():
        if i in visited:
            continue  # 如果当前节点已经处理过，跳过
        # 当前节点未处理，创建一个新的连通分量
        for j in dic[i]:
            if i in dic[j]:  # 强连通分量
                dic2[i].add(j)
                dic2[i].add(i)  # 将自己也加入到强连通分量
                visited.update(dic2[i])  # 标记所有属于该连通分量的节点为已处理
            # else:  # 弱连通分量
            #     if j not in visited:  # 确保 j 不重复
            #         dic2[j].add(j)
            #         visited.add(j)
        # 如果 i 未被标记，则添加自己为单独的弱连通分量
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