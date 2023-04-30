import re


def load(name):
    """
    Load the data

    params:
    name:   file directory and name
    """
    arr = []
    with open(name) as f:
        for i in f:
            x = [j.strip() for j in re.split(',|\[|\]', i)]
            xtmp = []
            xtmp.append(int(x[1]))
            xtmp.append(int(x[2]))
            xtmp.append(int(x[4]))
            xtmp.append(int(x[5]))
            arr.append(xtmp)

    return arr


# textArr.sort(key=takeSecond)
def takeSecond(arr):
    """
    Used as a key to return the 2nd element in an array

    params:
    arr:    input array
    """
    return arr[1]


# Credit to: https://www.programiz.com/dsa/kruskal-algorithm
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self, initial_edges):
        result = initial_edges[:]
        i, e = 0, len(initial_edges)
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        for k in result:
            u = k[0]
            v = k[1]
            w = k[2]
            x = self.find(parent, u)
            y = self.find(parent, v)
            self.apply_union(parent, rank, x, y)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        for u, v, weight in result:
            print("%d - %d: %d" % (u, v, weight))


g = Graph(6)
g.add_edge(0, 1, 4)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 2)
g.add_edge(1, 0, 4)
g.add_edge(2, 0, 4)
g.add_edge(2, 1, 2)
g.add_edge(2, 3, 3)
g.add_edge(2, 5, 2)
g.add_edge(2, 4, 4)
g.add_edge(3, 2, 3)
g.add_edge(3, 4, 3)
g.add_edge(4, 2, 4)
g.add_edge(4, 3, 3)
g.add_edge(5, 2, 2)
g.add_edge(5, 4, 3)

# Call Kruskal algorithm with initial edges
initial_edges = [[0, 1, 4], [2, 5, 2]]
g.kruskal_algo(initial_edges)



arr = load("./graf.txt")
