import time
import sys

def type_writer(message, delay=0.1):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the message

# Define the welcome message
welcome_message = "Welcome to Blackjack! Let's deal you some cards.\n"

# Call the type_writer function
type_writer(welcome_message, delay=0.05)

print("\033[1mWelcome to Blackjack! Let's deal you some cards.\n\033[0m")