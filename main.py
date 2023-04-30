import re


indices = {}


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
            xtmp2 = []
            xtmp2.append(int(x[4]))
            xtmp2.append(int(x[5]))
            arr.append(xtmp)
            arr.append(xtmp2)

    return arr


# textArr.sort(key=takeSecond)
def takeThird(arr):
    """
    Used as a key to return the 2nd element in an array

    params:
    arr:    input array
    """
    return arr[2]


def dist(x, y):
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    return abs(x2 - y2) + abs(x1 - y1)


def buildSet(arr):
    my_set = set()
    my_keys = []
    c = 0
    for i in arr:
        x = (i[0], i[1])
        if x not in my_set:
            my_set.add((i[0], i[1]))
            my_keys.append(c)
            c += 1
    l = list(my_set)
    return l, my_keys


def create_map(lst):
    indices = {}
    for i, x in enumerate(lst):
        indices[x] = i
    return indices


def find_index(element):
    return indices[element]


def allEdges(v):
    e = []
    for i in range(len(v)):
        for j in range(i + 1, len(v)):
            # e.append([v[i], v[j]])
            e.append([find_index((v[i])), find_index((v[j]))])
    return e


# Credit to: https://www.programiz.com/dsa/kruskal-algorithm
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def get(self):
        return self.graph

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


# g = Graph(6)
# g.add_edge(0, 1, 4)
# g.add_edge(0, 2, 4)
# g.add_edge(1, 2, 2)
# g.add_edge(1, 0, 4)
# g.add_edge(2, 0, 4)
# g.add_edge(2, 1, 2)
# g.add_edge(2, 3, 3)
# g.add_edge(2, 5, 2)
# g.add_edge(2, 4, 4)
# g.add_edge(3, 2, 3)
# g.add_edge(3, 4, 3)
# g.add_edge(4, 2, 4)
# g.add_edge(4, 3, 3)
# g.add_edge(5, 2, 2)
# g.add_edge(5, 4, 3)

# # Call Kruskal algorithm with initial edges
# initial_edges = [[0, 1, 4], [2, 5, 2]]
# g.kruskal_algo(initial_edges)


arr = load("./graph_2.txt")

myList, myKeys = buildSet(arr)
num_vertices = len(myList)
indices = create_map(myList)
#  print(indices)

edges = allEdges(myList)
# print(edges[:10])


g = Graph(num_vertices)
for i in range(0, len(arr), 2):
    g.add_edge(find_index(myList, (arr[i][0], arr[i][1])), find_index(myList, (arr[i + 1][0], arr[i + 1][1])), dist(arr[i], arr[i + 1]))

print(g.get())