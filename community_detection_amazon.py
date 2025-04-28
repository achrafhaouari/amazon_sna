import networkx as nx
from cdlib import algorithms, evaluation
import matplotlib.pyplot as plt
import random

# Load the graph
G = nx.read_gexf("amazon_copurchase_network.gexf")

# Community Detection Algorithms
louvain_coms = algorithms.louvain(G)
label_prop_coms = algorithms.label_propagation(G)
infomap_coms = algorithms.infomap(G)

# Evaluate Communities using Modularity
louvain_modularity = evaluation.newman_girvan_modularity(G, louvain_coms)
label_prop_modularity = evaluation.newman_girvan_modularity(G, label_prop_coms)
infomap_modularity = evaluation.newman_girvan_modularity(G, infomap_coms)

print(f"Louvain Modularity: {louvain_modularity.score:.3f}")
print(f"Label Propagation Modularity: {label_prop_modularity.score:.3f}")
print(f"Infomap Modularity: {infomap_modularity.score:.3f}")

# Visualize Community Sizes
plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.hist([len(c) for c in louvain_coms.communities], bins=20)
plt.title("Louvain Community Sizes")
plt.subplot(132)
plt.hist([len(c) for c in label_prop_coms.communities], bins=20)
plt.title("Label Propagation Community Sizes")
plt.subplot(133)
plt.hist([len(c) for c in infomap_coms.communities], bins=20)
plt.title("Infomap Community Sizes")
plt.tight_layout()
plt.savefig("community_sizes_amazon.png")
plt.close()

# Visualize Largest Community for Each Algorithm
def plot_community(G, community, title, filename):
    subgraph = G.subgraph(community)
    pos = nx.spring_layout(subgraph, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(subgraph, pos, node_size=50, node_color='lightblue', edge_color='gray', with_labels=False)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

# Largest communities
louvain_largest = max(louvain_coms.communities, key=len)
label_prop_largest = max(label_prop_coms.communities, key=len)
infomap_largest = max(infomap_coms.communities, key=len)

plot_community(G, louvain_largest, "Largest Louvain Community", "louvain_largest_community_amazon.png")
plot_community(G, label_prop_largest, "Largest Label Propagation Community", "label_prop_largest_community_amazon.png")
plot_community(G, infomap_largest, "Largest Infomap Community", "infomap_largest_community_amazon.png")

# Export Communities to GEXF for Gephi
G_communities = G.copy()
for i, community in enumerate(louvain_coms.communities):
    for node in community:
        G_communities.nodes[node]['louvain_community'] = i
for i, community in enumerate(label_prop_coms.communities):
    for node in community:
        G_communities.nodes[node]['label_prop_community'] = i
for i, community in enumerate(infomap_coms.communities):
    for node in community:
        G_communities.nodes[node]['infomap_community'] = i

nx.write_gexf(G_communities, "amazon_communities.gexf")
print("Network with community labels exported to 'amazon_communities.gexf' for Gephi")