def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
        
    # recursive call
    return fib(n-1) + fib(n-2)
    
print(fib(4))