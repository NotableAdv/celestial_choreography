# Question 2
# Given an array of integers, write a function that finds the second largest number in the array.

# importing libraries
import numpy
import random

# defining function to find the second highest numbers in array
def array_max(integers_np):

    #sorting the list of integers
    for j in range(len(integers_np)-1):
        for i in range(len(integers_np)-1):

            # compare two elements and swap if element 1 is greater
            if integers_np[i] > integers_np[i +1]:
                integers_np[i], integers_np[i+ 1] = integers_np[i+ 1], integers_np[i]

    # returning the integer second largest number, (so -2 for second)
    return integers_np[len(integers_np)-2]          


# creating a random list of 10 integers ranging 1-10
integers = []
for i in range(10):
    integers.append(random.randint(1,10))

# turning the list into an array
integers_np = numpy.array(integers)
print('Integers:', integers_np)

# printing out the seconf largest number
print("Second largest integer:", array_max(integers_np))



# Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote.

# The Big 0 notation for this code is O(n^2) because of the 2 for loops in the function. The n is the number of elements in the array (so 10).
