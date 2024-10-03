# Question 1
# Given an array of integers, write a function to calculate the sum of all elements in the array.

# importing libraries
import numpy
import random

# defining function to find total of array
def array_sum(intergers_np):
    total = 0

    # going through each number and adding it to the total
    for number in integers_np:
        total += number

    return total

# creating a random list of 10 integers ranging 1-10
integers = []
for i in range(10):
    integers.append(random.randint(1,10))

# turning the list into an array
integers_np = numpy.array(integers)
print('Integers:', integers_np)

# printing out the total
print("Total:", array_sum(integers_np))



# Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote.

# The Big 0 notation for this code is O(n). The n is the number of elements in the array (so 10). 
