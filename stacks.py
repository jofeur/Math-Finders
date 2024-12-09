class PlayerNode:
    def __init__(self, problem, solution):
        """Initialize a node that stores problem information."""
        self.problem = problem  # The math problem
        self.solution = solution  # The solution to the math problem
        self.next = None  # Pointer to the next node in the stack


class PlayerStack:
    def __init__(self):
        """Initialize the stack."""
        self.top = None  # The top of the stack, initially empty

    def push(self, problem, solution):
        """Push a new math problem node to the stack."""
        new_node = PlayerNode(problem, solution)  # Create a new node
        new_node.next = self.top  # Link the new node to the current top of the stack
        self.top = new_node  # The new node is now the top of the stack

    def pop(self):
        """Pop the top node from the stack and return the problem and solution."""
        if self.top is None:
            raise IndexError("pop from an empty stack")  # Raise an error if the stack is empty
        popped_node = self.top  # Get the current top node
        self.top = self.top.next  # Move the top pointer to the next node
        return popped_node.problem, popped_node.solution  # Return the problem and solution

    def peek(self):
        """Return the top problem and solution without removing the node."""
        if self.top is None:
            raise IndexError("peek from an empty stack")
        return self.top.problem, self.top.solution

    def is_empty(self):
        """Check if the stack is empty."""
        return self.top is None

    def display(self):
        """Display all problems in the stack (for debugging purposes)."""
        current = self.top
        print("Stack contents:")
        while current:
            print(f"Problem: {current.problem}, Solution: {current.solution}")
            current = current.next
