import sys

# The Messenger Bee's internal logic.
# It simply carries the message it is given.

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Join all arguments back together to handle messages with spaces.
        message = " ".join(sys.argv[1:])
        # Print the message so the calling shell script can capture it.
        print(message)
    else:
        print("ERROR: No message provided to the bee's core.")
