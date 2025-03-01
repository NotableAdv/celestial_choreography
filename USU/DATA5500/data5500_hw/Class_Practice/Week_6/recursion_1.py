# Recursion Example 1
pi = [3,1,4,5,9,2,6,5]

def print_lst(lst):
    for i in range(len(lst)):
        print(lst[i])

    return

print_lst(pi)

print("------------")

def print_rec(lst, start):
    # base case
    if start == len(lst) -1:
        return
    
    # solution logic    
    print(lst[start])

    #recursion call
    print_rec(lst, start +1)

    # return statement
    return

print_rec(pi, 0)