import numpy
import random

# create a list of 4 floats
homework_scores = [43.5, 48.3, 47.6, 50]
print(homework_scores)

# convert the list to a numpy array
hw_np = numpy.array(homework_scores)
print(hw_np)

# checkpoint activity
# create a list of 10 random numbers
lst = []
for i in range(10):
    lst.append(random.randint(1,100))
print('lst: ', lst)

# convert the list to a numpy array
lst_np = numpy.array(lst)
print('lst_np: ', lst_np)