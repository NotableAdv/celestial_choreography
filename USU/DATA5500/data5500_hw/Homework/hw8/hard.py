# Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5

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

# function to count the number of nodes with a degree above 5
def degree_check(g):
    count = 0

    # looking at the degree of each node
    for node, degree in g.degree():

        # adding 1 to the count if the degree is above 5
        if degree > 5:
            count += 1

    return count        

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

# checking the degree_check function
#print(degree_check(g))

# printing out the results of calling the function
print("Of the", count_nodes(g), "nodes,", degree_check(g), "have a degree greater than 5.")



# ChatGPT

# Pompt:
# "what is the syntax for using degree()"

# Output:
# The syntax for using the degree() method in NetworkX depends on whether you want to get the degree of all nodes or just a specific node:

# 1. Get the Degree of All Nodes
# G.degree() returns a view of the degree of each node in the graph.
# You can loop through it or convert it to a list or dictionary to see each node’s degree.

# for node, degree in G.degree():
#    print(f"Node {node} has a degree of {degree}")

# 2. Get the Degree of a Specific Node
# If you want the degree of a single node, pass the node as an argument to G.degree(node).

# print(G.degree(1))  # Outputs the degree of node 1

# 3. Get Degree as a Dictionary
# To store degrees as a dictionary for easy access, you can use a dictionary comprehension.

# degree_dict = dict(G.degree())
# print(degree_dict)

# 4. Weighted Degree (Optional)
# If your graph has weighted edges, you can pass weight="weight" to get the weighted degree, where edge weights are summed.

# weighted_degrees = G.degree(weight="weight")
# for node, degree in weighted_degrees:
#    print(f"Node {node} has a weighted degree of {degree}")

# These options let you get node degrees in different formats depending on your needs. Let me know if you have any other questions!