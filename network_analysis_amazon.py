import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# Load the graph from the GEXF file
print('load the graph from the GEXF ')
G = nx.read_gexf("amazon_copurchase_network.gexf")

# 1. Degree Distribution
print('Degree Distribution')
degrees = [degree for node, degree in G.degree()]
plt.hist(degrees, bins=40, log=True)
plt.title("Degree Distribution (Amazon Co-purchase)")
plt.xlabel("Degree")
plt.ylabel("Frequency (Log Scale)")
plt.savefig("degree_distribution_amazon.png")
plt.close()

# 2. Connected Components
print('Connected Components')
components = list(nx.connected_components(G))
num_components = len(components)
largest_component = max(components, key=len)
print(f"Number of connected components: {num_components}")
print(f"Size of largest component: {len(largest_component)}")

# 3. Path Analysis (Optimized)
print('Path Analysis (Optimized)')
largest_cc = G.subgraph(largest_component)

# Sample 100 nodes for average shortest path length
print('Sample 100 nodes for average shortest path length')
sample_size = 100
sampled_nodes = random.sample(list(largest_cc.nodes()), min(sample_size, len(largest_cc)))
total_path_length = 0
num_paths = 0
for node in sampled_nodes:
    lengths = nx.single_source_shortest_path_length(largest_cc, node)
    total_path_length += sum(lengths.values())
    num_paths += len(lengths) - 1  # Exclude path to self
avg_shortest_path = total_path_length / num_paths if num_paths > 0 else float('inf')
print(f"Estimated average shortest path length (sampled): {avg_shortest_path:.3f}")

# Approximate diameter by sampling 10 nodes
print('Approximate diameter by sampling 10 nodes')
sample_size_diameter = 10
sampled_nodes_diameter = random.sample(list(largest_cc.nodes()), min(sample_size_diameter, len(largest_cc)))
eccentricities = [nx.eccentricity(largest_cc, v) for v in sampled_nodes_diameter]
approx_diameter = max(eccentricities)
print(f"Approximate diameter (sampled): {approx_diameter}")

# 4. Clustering Coefficient and Density
print('Clustering Coefficient and Density')
avg_clustering = nx.average_clustering(G)
density = nx.density(G)
print(f"Average clustering coefficient: {avg_clustering:.3f}")
print(f"Network density: {density:.3f}")

# 5. Centrality Measures
print('Centrality Measures')
degree_centrality = nx.degree_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=500, tol=1e-06)

# Top 5 nodes by degree centrality
print('Top 5 nodes by degree centrality')
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 nodes by degree centrality:", top_degree)

# Top 5 nodes by eigenvector centrality
print('Top 5 nodes by eigenvector centrality')
top_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 nodes by eigenvector centrality:", top_eigenvector)