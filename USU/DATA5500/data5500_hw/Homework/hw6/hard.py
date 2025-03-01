# Question 3
# Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array.

# importing libraries
import numpy
import random

# defining function to find the range/difference of numbers in array
def array_range(integers_np):
    
    #sorting the list of integers
    for j in range(len(integers_np)-1):
        for i in range(len(integers_np)-1):

            # compare two numbers and swap if element 1 is greater
            if integers_np[i] > integers_np[i +1]:
                integers_np[i], integers_np[i+ 1] = integers_np[i+ 1], integers_np[i]

    # the top sorted value - the first sorted value
    difference = integers_np[len(integers_np)-1] - integers_np[0]

    return difference

# creating a random list of 10 integers ranging 1-10
integers = []
for i in range(10):
    integers.append(random.randint(1,10))

# turning the list into an array
integers_np = numpy.array(integers)
print('Integers:', integers_np)

# printing out the range
print("Max distance of numbers:", array_range(integers_np))
 


# Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote.

# The Big 0 notation for this code is O(n^2) because of the 2 for loops in the function. The n is the number of elements in the array (so 10).
