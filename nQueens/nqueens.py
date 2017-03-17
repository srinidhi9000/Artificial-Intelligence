#Srinidhi Krishnan
#5
#2018skrishna2@tjhsst.edu
#11/2/16
import time
import math
from collections import deque
import random
gt = 0
nt = 0
n = 5


class nQueens:
    def __init__(self, state, parent):
        """ creates an nQueens board where state is a list of n integers,
            one per column,
            and choices is a list of sets,
            n is the size
            parent is the state predecessor in a search
        """
        self.state = state
        self.choices = [set(range(1, n + 1))] * n
        if parent != None:
            for i in range(n):
                se = set(parent.choices[i])
                self.choices[i] = se
        self.parent = parent

    def assign(self, var, value):
        """ updates the state by setting state[var] to value, also propagates constraints and updates choices
            remove all values from var so best first search doesn't return the same col multiple times
            remove value from each column (making sure the queens can't attack horizontally)
            remove diagonals: dy is y2-y1, so x1+-dy should be a diagonal.
            even if value+-dy is out of range, difference_update won't cause any set errors
            """
        self.state[var] = value

        for c in range(n):
            self.choices[c].difference_update([value])
            dy = c - var
            se = set(self.choices[c])
            se.difference_update([value + dy, value - dy])
            self.choices[c] = se
        se1 = {}
        self.choices[var] = se1

    def get_next_unassigned_var(self):
        """ returns the index of a column that is unassigned and has valid choices available """
        # fastest
        # best first search
        min = -1
        for i in range(n):
            if self.state[i] == 0:
                if min == -1:
                    min = i
                elif len(self.choices[i]) < len(self.choices[min]):
                    min = i
        return min

        # 2: Start at random col
        """while True:
            i = random.randint(0, n - 1)
            if self.state[i] == 0:
                return i
"""
        # 3: Start at the first col
        """for i in range(len(self.state)):
                if self.state[i] == 0:
                    return i
        """
        # slowest

    def get_choices_for_var(self, var):
        """ returns choices[var], the list of available values
                 for variable var, randomly sorted """
        l = list(self.choices[var])
        """cost = n - int(n/2)
        l.sort(key = lambda n:cost) middle distance not fast enough"""
        random.shuffle(l)
        return l
        #return self.choices[var]

    def __str__(self):
        """ returns a string representation of the object """
        return self.state()

    def goal_test(self):
        """ returns True iff state is the goal state and increment goal test counter"""
        global gt
        gt +=1
        for i in self.state:
            if i == 0:
                return False
        print(self.state)
        return True

###---------------------------------------------------------------


def dfs_search():
    """depth first search for n queens"""
    global nt
    fringe = deque()
    fringe.append(nQueens([0] * n, None))
    while True:
        if len(fringe) == 0:
            return False
        current = fringe.pop()
        if current.goal_test():
            return current
        var = current.get_next_unassigned_var()
        for value in current.get_choices_for_var(var):
            child = nQueens(list(current.state), current)
            nt += 1
            child.assign(var, value)
            fringe.append(child)


if __name__ == "__main__":
    for i in range(4,29):
        n = i
        gt = 0
        nt = 0
        print(n)
        start_time = time.time()
        s = dfs_search()
        end_time = time.time()
        duration = end_time - start_time
        print("Goal tests:" + str(gt))
        print("Nodes Created:" + str(nt))
        print("Time:" + str(duration))
        print()

