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

    # def get(self):
    #     return self.graph


arr = load("./graf.txt")
# g = Graph(3)
# g.add_edge([arr[0][0], arr[0][1]], [arr[0][2], arr[0][3]], 5)
# g.add_edge([arr[1][0], arr[1][1]], [arr[1][2], arr[1][3]], 5)
# g.add_edge([arr[2][0], arr[2][1]], [arr[2][2], arr[5][3]], 5)
# print(g.get())