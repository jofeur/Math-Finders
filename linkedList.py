class Node:
    def __init__(self, problem, solution):
        self.problem = problem  
        self.solution = solution  
        self.next = None  


class MathLinkedList:
    def __init__(self):
        self.head = None  

    def add_problem(self, problem, solution):
        new_node = Node(problem, solution)
        if not self.head: 
            self.head = new_node
        else:
            current = self.head
            while current.next: 
                current = current.next
            current.next = new_node  

    def get_problem(self):
        if not self.head:  
            return None, None
        problem, solution = self.head.problem, self.head.solution
        self.head = self.head.next 
        return problem, solution

  

