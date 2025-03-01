# Medium Question

# Create a class called Employee with attributes name and salary. 
class Employee:
    def __init__(self, name, salary, raise_percent):
        self.name = name
        self.salary = salary
        self.raise_percent = raise_percent
    
    # Implement a method within the class that increases the salary of the employee by a given percentage. 
    def __str__(self):
        self.new_salary = self.salary * (1 + self.raise_percent)
        return self.name + "'s new salary is $" + str(self.new_salary)

# Instantiate an object of the Employee class with name = "John" and salary = 5000, increase the salary by 10%, and print the updated salary.    
employee_1 = Employee ("John", 5000, 0.10)

print(employee_1)
