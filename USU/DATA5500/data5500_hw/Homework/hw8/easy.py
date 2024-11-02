# Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph.

# importing libraries
import os
import networkx as nx

# importing libraries to plot the graph
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# finding the current directory
curr_dir = os.path.dirname(__file__)

# file the edge information is stored in
edges_txt = curr_dir + "/" + "edges.txt"
file = open(edges_txt)

# function to count the number of nodes in the graph
def count_nodes(g):
    return len(g.nodes)

# blank list of the edges
edges = []

# adding each line of the text file into the edges list
for line in file:
    node1, node2, weight = line.split(",")
    weight = int(weight)
    edges.append((node1,node2,weight))

# checking the edges list
#print(edges)

# creating the graph using the edges list
g = nx.DiGraph()
g.add_weighted_edges_from(edges)

# file the graph will be added to
graph_visual_fil = curr_dir + "/" + "graph_visual.png"

# visualizing the graph
pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

# saving the graph to the file
plt.savefig(graph_visual_fil)

# checking the count_nodes function
#print(count_nodes(g))

# printing out the results of calling the function
print("There are", count_nodes(g), "nodes")
