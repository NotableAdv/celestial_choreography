# Recursion Example 3
#Factorial 

def factorial(n):
    total = 1
    for i in range(1, n+1):
        total *= i

    return total

print(factorial(5))

def factorial_rec(n):
    if n==1:
        return n
    
    return n * factorial_rec(n-1)

print(factorial_rec(5))