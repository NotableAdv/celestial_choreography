# Implement a Python function to search for a value in a binary search tree. 
# The method should take the root of the tree and the value to be searched as parameters. 
# It should return True if the value is found in the tree, and False otherwise.

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

# Search function to find a key in the binary search key
def findKey(root, searchkey):
    
    # Base case: root is None or the key is found
    if root is None:
        return False  # Key not found
    if root.key == searchkey:
        return True  # Key found

    # Recursively search in the left or right subtree
    if searchkey < root.key:
        return findKey(root.left, searchkey)
    else:
        return findKey(root.right, searchkey)

# Main function to create random tree and search
def main():
    
    # creating a Tree with root variable "root"
    root = None

    # Insert 10 random values between 1 and 25 into the tree
    for i in range(10):
        random_value = random.randint(1,25)
        root = insert(root, random_value)

    # Print the binary tree - used to test searches	
    # display(root)
    
	# Loop to search for values
    while True:
        
		# callinf the search and printing the results
        answer = findKey(root, int(input("What number would you like to look for? (1 to 25): ")))
        print(answer, '\n') 
        
		# Prompting if the user still wants to search
        searching = input('Press y to keep searching (any other key to quit): ')
        
		# exit the loop if they don't put y
        if searching != 'y':
            break
        
        else:
            print()


# calling function to create and search a random tree
main()