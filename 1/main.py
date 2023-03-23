import math


def load(name):
    """
    Load the data

    params:
    name:   file directory and name
    """
    arr = []
    with open(name) as f:
        for i in f:
            x = [j.strip() for j in i.split()]
            x[0] = int(x[0])
            arr.append(x)

    return arr


def takeSecond(arr):
    """
    Used as a key to return the 2nd element in an array

    params:
    arr:    input array
    """
    return arr[1]


def generate_params(textArr):
    """
    Calculate qi and pi probabilities and sorted strings of all words with frequency > 50000
    Returns a set of probabilities selecting a high frequency word (pi), probabilities selecting a high frequency word (qi),
    and keys high frequency words (str)

    params:
    textArr:    Dictionary
    """
    textArr.sort(key=takeSecond)
    sum_f = sum([textArr[i][0] for i in range(len(textArr))])
    n = len(textArr)

    pi, qi, str = [], [], []
    p, s, dummy = [0], [""], 0

    for i in textArr:
        if i[0] > 50000:
            pi.append(p[0])
            qi.append(dummy / sum_f)
            str.append(s[0])

            p.append(i[0] / sum_f)
            s.append(i[1])

            dummy = 0
            p.pop(0)
            s.pop(0)
        else:
            dummy += i[0]

    pi.append(p[0])
    qi.append(dummy / sum_f)
    str.append(s[0])
    return pi, qi, str


def generate_tree(pi, qi, n):
    """
    Generate root and e matrix based on algorithm described in Optimal-BST str. 419 15.5 Introduction to Algorithms
    Code inspired from: https://www.geeksforgeeks.org/optimal-binary-search-tree-dp-24/
    Returns a generated tree as an array

    params:
    pi:     probability of selecting a word from a sorted list of words with frequency greater than 50000.
    qi:     probability of selecting a word from the low-frequency words after selecting a word from the high-frequency words
    n:      size of pi
    """
    cost = [[0 for i in range(n)] for j in range(n + 1)]
    prob_sum = [[0 for i in range(n)] for j in range(n + 1)]
    root = [[0 for i in range(n)] for j in range(n)]

    for i in range(1, n + 1):
        cost[i][i - 1] = qi[i - 1]
        prob_sum[i][i - 1] = qi[i - 1]

    for l in range(1, n):
        for i in range(1, n - l + 1):
            j = i + l - 1
            cost[i][j] = math.inf
            prob_sum[i][j] = prob_sum[i][j - 1] + pi[j] + qi[j]

            for r in range(i, j + 1):
                t = cost[i][r - 1] + cost[r + 1][j] + prob_sum[i][j]
                if t < cost[i][j]:
                    cost[i][j] = t
                    root[i][j] = r
    return cost, root


def search_tree(root, str, start, end, s, count):
    """
    Search the tree recursively and calculate the dept (i.e. number of comparisons) and return the results
    If the given word is not found, it returns (None, depth)
    
    params: 
    root:      generated tree
    str:       array of keys with high frequency
    start:     integer representing the starting index of the range of keys for the current subtree being searched
    end:       integer representing the ending index of the range of keys for the current subtree being searched
    s:         string representing the key being searched in the current subtree
    count:     counter of the number of depth
    """
    if start > end or end <= 0 or root[start][end] == None:
        return None, count

    root_s = str[root[start][end]]

    if (not root_s) or (len(root_s) == 0) or (root_s == s):
        return root_s, count + 1
    
    if s < root_s:
        return search_tree(root, str, start, root[start][end] - 1, s, count + 1)
    
    return search_tree(root, str, root[start][end] + 1, end, s, count + 1)


def pocet_porovnani(s, root, str):
    """
    Returns a number of comparisons for a given word

    params: 
    root:      generated tree
    str:       array of keys with high frequency
    s:         string representing the key being searched in the current subtree
    """
    if len(s) == 0:
        return None, 0
    found_key, count = search_tree(root, str, 1, len(root) - 1, s, 0)
    return found_key, count


def branches(root, str):
    """
    Print the tree

    params:
    root:       generated tree
    str:        array of keys with high frequency
    """
    branches = []
    for s in str:
        s, branch = pocet_porovnani(s, root, str)
        branches.append([s, branch])

    for i in branches:
        if not(i[0]):
            branches.remove(i)

    branches.sort(key=takeSecond)
    current_level = 0

    for branch in branches:
        level = branch[1]
        if(current_level < level):
            current_level = level
            if(branch[1] == 1):
                print(f"Root:")
                print(f"\t-{branch[0]}")
                continue
            print(f"Branch {branch[1]}:")
        print(f"\t-{branch[0]}")


if __name__ == "__main__":
    textArr = load("dictionary.txt")
    pi, qi, str = generate_params(textArr)
    cost, root = generate_tree(pi, qi, len(pi))
    branches(root, str)

    while True:
        print("Enter the search string (or esc to exit): ")
        inpt = input()
        if(inpt == 'esc'):
            break
        print(pocet_porovnani(inpt, root, str))
