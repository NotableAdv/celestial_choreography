# Stack implementation
stack = []

# Adding items to the stack
stack.append(3)
stack.append(4)
stack.append(5)

print("Stack after pushing:", stack)

# Removing items from the stack
last_item = stack.pop()
print("Popped from stack:", last_item)
print("Stack after popping:", stack)

# Queue implementation
queue = []

# Adding items to the queue
queue.append(3)
queue.append(4)
queue.append(5)

print("Queue after enqueuing:", queue)

# Removing items from the queue
first_item = queue.pop(0) 
print("Dequeued from queue:", first_item)
print("Queue after dequeuing:", queue)
