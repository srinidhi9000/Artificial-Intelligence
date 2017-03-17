import time
import pickle
import string

_goal_state = ""
_count = 0
_d = set()
soln = open('solutions.txt', 'w')


class Node:
    def __init__(self, state, parent, depth, action, cost):
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
            n = n.parent
            sol.append(n)
        sol.reverse()
        actions = ""
        for s in sol:
            actions += s.action
        return[i.state for i in sol]

    def expand(self):
        for i in range(0,6):
            word = list(self.state)
            for c in string.ascii_lowercase:
                word[i]=c
                ns = ''.join(word)
                if ns+'\n' in _d:
                    self.add_child(Node(ns, self, self.depth +1, ns, 0))
        return self.children

    def add_child(self, node):
        n = self
        while n.state != node.state and n.parent is not None:
            n = n.parent
        if n.state != node.state:
            self.children.append(node)


def tree_search():
    f = open('dict.txt')
    for line in f:
        _d.add(line)
    fringe = [Node(_start_state, None, 0, "", 0)]
    f.close()
    while True:
        if len(fringe) == 0:
            return "No solution"
        n = fringe.pop(0)
        if n.goal_test():
            print(n.get_solution())
            return "Solved"
            soln.write(_start_state + " " + _goal_state)
        fringe.extend(n.expand())

if __name__ == "__main__":
    solution = "?"
    file = open('puzzlesA.txt')
    for line in file:
        print(line)
        words = line.split(" ")
        _start_state = words[0]
        _goal_state = words[1].strip()
        start_time = time.time()
        s = tree_search()
        end_time = time.time()
        duration = end_time - start_time
        print(duration)
        soln.write(str(duration))
    file.close()
