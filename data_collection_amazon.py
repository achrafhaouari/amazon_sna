import networkx as nx
import urllib.request
import gzip
import shutil

# Load the undirected graph
G = nx.read_edgelist("amazon0302.txt", comments="#", nodetype=int, create_using=nx.Graph())

# Filter to top 3,000 nodes by degree
degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
top_nodes = [node for node, degree in degrees[:3000]]
G = G.subgraph(top_nodes)

# Verify the network size
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Export to GEXF for Gephi
nx.write_gexf(G, "amazon_copurchase_network.gexf")
print("Network exported to 'amazon_copurchase_network.gexf' for Gephi")