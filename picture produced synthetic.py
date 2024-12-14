import networkx as nx
import matplotlib.pyplot as plt
import timeit

from Connectors_Version_2 import fast_strong_connector  # Ensure the module is imported correctly

# Create graph sizes from 1000 to 40000 with an interval of 1000
graph_sizes = range(1000, 40001, 1000)
vertices_and_edges = []  # Store the sum of total nodes and edges for each graph
times = []  # Store execution times
m_plus_n = []  # Store the value of m + n

# Test the execution time of fast_strong_connector for each graph
for size in graph_sizes:
    print(f"Generating scale-free graph with {size} nodes...")
    graph = nx.scale_free_graph(size)  # Generate a scale-free graph
    total_nodes = len(graph.nodes)  # Number of nodes in the graph
    total_edges = len(graph.edges)  # Number of edges in the graph
    vertices_and_edges.append(total_nodes + total_edges)  # Sum of nodes and edges

    # Measure execution time and retrieve m and n
    start_time = timeit.default_timer()
    P, m, n = fast_strong_connector(graph, final_readout=True)
    elapsed_time = timeit.default_timer() - start_time

    times.append(elapsed_time)
    m_plus_n.append(m + n)
    print(f"Graph with {total_nodes} nodes and {total_edges} edges (total={total_nodes + total_edges}) took {elapsed_time:.4f} seconds")
    print(f"m + n = {m + n}")

# Plot the first curve: Total nodes and edges vs execution time
plt.figure(figsize=(12, 6))
plt.plot(vertices_and_edges, times, marker='o', label='Runtime vs Total Vertices and Edges')
plt.title("Runtime of fast_strong_connector vs Total Vertices and Edges")
plt.xlabel("Total Number of Nodes and Edges")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

# Plot the second curve: m + n vs execution time
plt.figure(figsize=(12, 6))
plt.plot(m_plus_n, times, marker='o', label='Runtime vs m + n', color='orange')
plt.title("Runtime of fast_strong_connector vs m + n")
plt.xlabel("m + n (Sources + Sinks)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Assume vertices_and_edges, times, and m_plus_n have been generated
vertices_and_edges = np.array(vertices_and_edges).reshape(-1, 1)
m_plus_n = np.array(m_plus_n).reshape(-1, 1)
times = np.array(times)

# Define a function: Filter outliers and fit the data
def filter_and_fit(x, y, title, xlabel, color):
    # Calculate z-scores
    mean_y = np.mean(y)
    std_y = np.std(y)
    z_scores = (y - mean_y) / std_y

    # Define z-score threshold, usually set to 3
    threshold = 3
    filtered_indices = np.abs(z_scores) < threshold

    # Filtered data
    x_filtered = x[filtered_indices]
    y_filtered = y[filtered_indices]

    # Polynomial fitting
    poly_features = PolynomialFeatures(degree=2)  # Quadratic polynomial
    X_poly = poly_features.fit_transform(x_filtered)
    model = LinearRegression().fit(X_poly, y_filtered)
    y_pred = model.predict(X_poly)
    r2 = r2_score(y_filtered, y_pred)

    # Plot the filtered curve
    plt.figure(figsize=(12, 6))
    plt.scatter(x_filtered, y_filtered, color=color, label='Filtered Data')
    plt.plot(x_filtered, y_pred, color='red', label=f'Fit (R²={r2:.4f})')
    plt.title(f"Runtime vs {xlabel} (Filtered)")
    plt.xlabel(xlabel)
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return model, r2


# Filter and fit "Total Nodes + Edges" vs "Time"
filter_and_fit(vertices_and_edges, times,
               title="Runtime vs Total Vertices and Edges (Filtered)",
               xlabel="Total Nodes + Edges", color='blue')

# Filter and fit "m + n" vs "Time"
filter_and_fit(m_plus_n, times,
               title="Runtime vs m + n (Filtered)",
               xlabel="m + n (Sources + Sinks)", color='orange')
