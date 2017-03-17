import time

_goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9]
_maxtiles = 9
_count = 0

class Node:

    def __init__(self, state, parent, depth, action, cost):
        "Create a search tree Node, derived from a parent by an action."
        self.state = state
        self.parent = parent
        self.depth = depth
        self.action = action
        self.cost = cost
        self.children = []

    def display(self):
        print(self.state, self.action)

    def goal_test(self):
        global _count
        _count += 1
        return self.state == _goal_state

    def get_solution(self):
        n = self
        sol = [n]
        while n.parent is not None:
            n=n.parent
            sol.append(n)
        sol.reverse()
        actions = ""
        for s in sol:
            actions += s.action
        print("Solution...", actions)
        return[i.state for i in sol]

    def swap_blank(self, a, b):
        new_state = self.state.copy()
        t = new_state[a]
        new_state[a] = new_state[b]
        new_state[b] = t
        return new_state

    def expand(self):
        blank_index = self.state.index(_maxtiles)
        row = blank_index//3
        col = blank_index%3

        if col < 2:
            new_state = self.swap_blank(blank_index, blank_index + 1)
            action = "R"
            self.add_child(Node(new_state, self, self.depth + 1, action, 0))
        if col > 0:
            new_state = self.swap_blank(blank_index, blank_index - 1)
            action = "L"
            self.add_child(Node(new_state, self, self.depth + 1, action, 0))
        if row < 2:
            new_state = self.swap_blank(blank_index, blank_index + 3)
            action = "D"
            self.add_child(Node(new_state, self, self.depth + 1, action, 0))
        if row > 0:
            new_state = self.swap_blank(blank_index, blank_index - 3)
            action = "U"
            self.add_child(Node(new_state, self, self.depth + 1, action, 0))
        return self.children

    def add_child(self, node):
        n = self
        while n.state != node.state and n.parent is not None:
            n = n.parent
        if n.state != node.state:
            self.children.append(node)

def tree_search():
    fringe = [Node(_start_state, None, 0,"",0)]
    while True:
        if len(fringe) == 0:
            return "No soloution"
        n = fringe.pop(0)
        if n.goal_test():
            print(n.get_solution())
            return "Solved"
        fringe.extend(n. expand())

if __name__ == "__main__":
    solution = "?"
    _start_state = [2,4,3,1,9,6,7,5,8]
    solution = solution.replace("U", "d").replace("D", "u").replace("L", "r").replace("R", "l").upper()
    s = tree_search()

        
