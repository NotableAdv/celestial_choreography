# Write a Python function to insert a value into a binary search tree. 
# The function should take the root of the tree and the value to be inserted as parameters.

import random

from print_tree import * 

# Node class for the binary tree search
class Node:

	# Constructor to create a new node
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None
		
# Insert function for the binary search tree
def insert(node, key):

	# If the tree is empty, return a new node
	if node is None:
		return Node(key)

	# Otherwise recur down the tree
	if key < node.key:
		node.left = insert(node.left, key)
		  
	elif key > node.key:
		node.right = insert(node.right, key)

	# return the (unchanged) node pointer
	return node


# Function to create the tree
def main():
	
    # creating a Tree with root variable "root"
    root = None

    # Insert 10 random values between 1 and 25 into the tree
    for i in range(10):
        random_value = random.randint(1,25)
        root = insert(root, random_value)

    # calling the imported function to print the tree	
    display(root)


# Calling function to create a random tree
main()