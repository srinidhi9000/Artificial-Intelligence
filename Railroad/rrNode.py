import time
import sys
import heapq
from math import pi, acos, sin, cos

bigDict = {}
nodeDict = {}
cities = {}
goal_state = ""
start_state = ""
soln = open('solutions.txt', 'w')


class Node:
    def __init__(self, state, parent, f):
        self.state = state
        self.parent = parent
        self.f = f
        self.g = 0
        self.h = 0

    def __lt__(self, node):
        return self.f < node.f

    def expand(self):
        successors = set()
        for c in bigDict[self.state]:
            s = Node(c, None, 0)
            s.parent = self
            s.g = self.g + bigDict[self.state][c]
            s.h = distance(s.state, goal_state)
            s.f = s.g + s.h
            successors.add(s)
        return successors


    def add_child(self, node):
        n = self
        while n.state != node.state and n.parent is not None:
            n = n.parent
        if n.state != node.state:
            bigDict[self.state].append(node)

    def solution(self):
        "Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def distance(s1, s2):
    x1 = nodeDict[s1][1]
    y1 = nodeDict[s1][0]
    x2 = nodeDict[s2][1]
    y2 = nodeDict[s2][0]
    R = 3958.76  # miles
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    return acos(min(1, sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1))) * R


def addEdge(s1, s2):
    if s1 not in bigDict:
        bigDict[s1] = {}
    if s2 not in bigDict:
        bigDict[s2] = {}
    d = distance(s1, s2)
    bigDict[s1][s2] = d
    bigDict[s2][s1] = d


def makeGraph():
    file1 = open('rrNodes.txt')
    for line in file1:
        a = line.split(" ")
        a[2] = a[2].rstrip('\n')
        nodeDict[a[0]] = (float(a[1].rstrip('\n')), float(a[2].rstrip('\n')))
    file2 = open('rrEdges.txt')
    for line in file2:
        a = line.split(" ")
        addEdge(a[0].rstrip('\n'), a[1].rstrip('\n'))

def cityMap():
    infile = open("rrCities.txt","r")
    for line in infile.readlines():
        line = line.strip("\n")
        (id, *name) = line.split(" ")
        cityName = " ".join(name)
        cities[cityName] = id
        # do something with cityName and ID!
    infile.close()



def tree_search():
    closed = set()
    dist = 0
    fringe = [Node(start_state, None, 0)]
    while True:
        if not fringe:
            return None
        node = heapq.heappop(fringe)
        if node.state == goal_state:
            return node.f
        if node.state not in closed:
            closed.add(node.state)
            for x in node.expand():
                heapq.heappush(fringe, x)


import time
if __name__ == "__main__":
    makeGraph()
    cityMap()
    str = ""
    #start_state = input("Station 1: ")
    #goal_state = input("Station 2: ")
    infile = open("test.txt","r")
    for line in infile.readlines():
        line = line.strip("\n")
        (s1, s2) = line.split(", ")
        start_state = cities[s1]
        goal_state = cities[s2]
        if start_state in nodeDict and goal_state in nodeDict:
            #print(distance(start_state, goal_state))
            s = time.time()
            dist = tree_search()
            e = time.time()
            t = e - s

            print("%20s %20s %8.3f %4.3f" % (s1, s2, dist, t))
            str += ("%20s %20s %8.3f %4.3f" % (s1, s2, dist, t))
            str+= "\n"
        else:
            print("Station not valid")
    outfile = open("solutions.txt","w")
    print(str, file=outfile)
    infile.close()

