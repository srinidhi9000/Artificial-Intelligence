# Srinidhi Krishnan
# 5
# 2018skrishna2@tjhsst.edu
# 11/2/16
import time
import math
from collections import deque
import random

"""start_state = [8, -1, -1, -1, -1, -1, -1, -1, -1,
               -1, -1, -1, -1, -1, -1, 5, -1, 7,
               -1, -1, -1, -1, -1, -1, -1, 6, 1,
               -1, 1, -1, -1, 8, 6, 9, -1, 5,
               -1, -1, -1, -1, 1, 4, -1, -1, -1,
               -1, 9, 6, 5, -1, -1, -1, -1, 4,
               -1, -1, 8, -1, -1, 7, -1, -1, -1,
               7, 5, -1, 3, -1, -1, -1, -1, 9,
               -1, -1, 9, -1, -1, 1, 3, -1, -1]"""
start_state = [3,-1, -1, -1, 8,-1, -1, -1, -1, -1, -1, -1, 7,-1, -1, -1, -1, 5,1,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3,6,-1, -1, -1, 2,-1, -1, 4,-1, -1, -1, -1, 7,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6,-1, 1,3,-1, -1, 4,5,2,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8,-1, -1]
gt = 0
nt = 0
n = 9


class sudoku:
    def __init__(self, state, parent):
        """ creates an sudoku board where state is a list of n integers,
            one per column,
            and choices is a list of sets,
            n is the size
            parent is the state predecessor in a search
        """
        self.state = state
        self.choices = [set(range(1, n + 1)) for i in range(81)]
        if parent != None:
            for i in range(81):
                se = set(parent.choices[i])
                self.choices[i] = se
        else:
            self.makeBoard(start_state)
        self.parent = parent

    def assign(self, var, value):
        self.state[var] = value
        row = var // n
        col = var % n
        j = col
        # updates everything in same row
        for i in range(n * row, n * (row + 1)):
            self.choices[i].difference_update([value])
        # updates everything in same col
        while j < 81:
            self.choices[j].difference_update([value])
            j += n
        # updates everything in box
        for k in self.getBox(var):
            self.choices[k].difference_update([value])

    def makeBoard(self, arr):
        for i in range(len(arr)):
            if arr[i] != -1:
                self.assign(i, arr[i])

    def getBox(self, var):
        if var < 27:
            if var % n < 3:
                return [0, 1, 2, 9, 10, 11, 18, 19, 20]
            elif var % n > 5:
                return [6, 7, 8, 15, 16, 17, 24, 25, 26]
            else:
                return [3, 4, 5, 12, 13, 14, 21, 22, 23]
        elif var > 53:
            if var % n < 3:
                return [54, 55, 56, 63, 64, 65, 72, 73, 74]
            elif var % n > 5:
                return [60, 61, 62, 69, 70, 71, 78, 79, 80]
            else:
                return [57, 58, 59, 66, 67, 68, 75, 76, 77]
        else:
            if var % n < 3:
                return [27, 28, 29, 36, 37, 38, 45, 46, 47]
            elif var % n > 5:
                return [33, 34, 35, 42, 43, 44, 51, 52, 53]
            else:
                return [30, 31, 32, 39, 40, 41, 48, 49, 50]

    def get_next_unassigned_var(self):
        """ returns the index of a column that is unassigned and has valid choices available """
        # fastest
        # best first search
        min = -2
        for i in range(81):
            if self.state[i] == -1:
                if min == -2:
                    min = i
                elif len(self.choices[i]) < len(self.choices[min]):
                    min = i
        return min
        """for i in range(len(self.state)):
            if self.state[i] == -1:
                return i"""

    def get_choices_for_var(self, var):
        """ returns choices[var], the list of available values
                 for variable var, randomly sorted """
        l = list(self.choices[var])
        random.shuffle(l)
        return l

    def __str__(self):
        """ returns a string representation of the object """
        return self.state()

    def goal_test(self):
        """ returns True iff state is the goal state and increment goal test counter"""
        global gt
        gt += 1
        for i in self.state:
            if i == -1:
                return False
        s = ""
        for i in range(81):
            s += str(self.state[i])
            s += " "
            if i % 3 == 2:
                s += "|"
            if i % n == 8:
                s += "\n"
            if i % 27 == 26:
                s += "---------------------\n"
        print(s)
        return True


###---------------------------------------------------------------


def dfs_search():
    """depth first search for n queens"""
    global nt
    fringe = deque()
    fringe.append(sudoku(start_state, None))
    while True:
        if len(fringe) == 0:
            print("No Solution")
            return False
        current = fringe.pop()
        if current.goal_test():
            return current
        var = current.get_next_unassigned_var()
        for value in current.get_choices_for_var(var):
            child = sudoku(list(current.state), current)
            nt += 1
            child.assign(var, value)
            fringe.append(child)


if __name__ == "__main__":
    gt = 0
    nt = 0
    start_time = time.time()
    s = dfs_search()
    end_time = time.time()
    duration = end_time - start_time
    print("Goal tests:" + str(gt))
    print("Nodes Created:" + str(nt))
    print("Time:" + str(duration))
    print()
