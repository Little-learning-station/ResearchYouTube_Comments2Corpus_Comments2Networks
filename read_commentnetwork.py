#1. Robust loader for GDF graph format

#This version auto-detects the node and edge sections:

import pandas as pd

file_path = "Yourvideocommentnetwork.gdf"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# locate sections
node_idx = [i for i,l in enumerate(lines) if l.lower().startswith("nodedef")][0]
edge_idx = [i for i,l in enumerate(lines) if l.lower().startswith("edgedef")][0]

# extract column names
node_cols = lines[node_idx].strip().split(">")[1]
edge_cols = lines[edge_idx].strip().split(">")[1]

# read tables separately
nodes = pd.read_csv(
    file_path,
    skiprows=node_idx+1,
    nrows=edge_idx-node_idx-1,
    names=node_cols.split(","),
    engine="python"
)

edges = pd.read_csv(
    file_path,
    skiprows=edge_idx+1,
    names=edge_cols.split(","),
    engine="python"
)

print(nodes.head())
print(edges.head())


# 2. Build the graph
import networkx as nx

G = nx.from_pandas_edgelist(
    edges,
    source=edges.columns[0],
    target=edges.columns[1]
)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

#3. Basic visualization

import matplotlib.pyplot as plt

plt.figure()
nx.draw(
    G,
    with_labels=False,
    node_size=20
)

plt.show()

#This format GraphML is supported by Gephi. So open this file in Gephi and try ForceAtlas2 to play out the comment networks 
nx.write_graphml(G, "yourgraphname.graphml")
