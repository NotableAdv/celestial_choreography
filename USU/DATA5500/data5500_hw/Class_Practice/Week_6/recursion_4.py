# Recusion Example 4
# Fibonacci


def fibonacci(n):
    f1 = 1
    f2 = 1
    tmp = 1
    for i in range(1, int(n)-1):
        tmp = f1+f2
        f1 = f2
        f2=tmp
    return f2

print(fibonacci(20))

def fibonacci_rec(n):
    if n < 2:
        return n
    
    return fibonacci_rec(n-1) + fibonacci_rec(n-2)

print(fibonacci_rec(20))    