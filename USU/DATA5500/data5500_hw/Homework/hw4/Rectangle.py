# Easy Question

# Create a class called Rectangle with attributes length and width. 
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    # Implement a method within the class to calculate the area of the rectangle.
    def __str__(self):
        self.area = self.length * self.width
        return "The area is " + str(self.length) + " x " + str(self.width) + " = " + str(self.area)

# Instantiate an object of the Rectangle class with length = 5 and width = 3, and print its area.
rectangle = Rectangle (5, 3)

print(rectangle)
