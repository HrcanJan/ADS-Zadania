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

    pi = []
    qi = []
    str = []
    dummy_f = 0
    p = [0]
    s = [""]

    for i in range(len(textArr)):
        if textArr[i][0] > 50000:

            pi.append(p.pop())
            qi.append(dummy_f / sum_f)
            str.append(s.pop())
            p.append(textArr[i][0] / sum_f)
            s.append(textArr[i][1])
            dummy_f = 0
        else:
            dummy_f += textArr[i][0]

    pi.append(p.pop())
    qi.append(dummy_f / sum_f)
    str.append(s.pop())
    return pi, qi, str


def generate_tree(pi, qi):
    """
    Generate root and e matrix based on algorithm described in Optimal-BST str. 419 15.5 Introduction to Algorithms
    Code inspired from: https://www.geeksforgeeks.org/optimal-binary-search-tree-dp-24/
    Returns a generated tree as an array

    params:
    pi:     probability of selecting a word from a sorted list of words with frequency greater than 50000.
    qi:     probability of selecting a word from the low-frequency words after selecting a word from the high-frequency words
    """
    n = len(pi)

    root = [[0 for i in range(n)] for j in range(n)]
    prob_sum = [[0 for i in range(n)] for i in range(n + 1)]
    expect_cost = [[0 for i in range(n)] for i in range(n + 1)]

    for i in range(1, n + 1):
        prob_sum[i][i - 1] = qi[i - 1]
        expect_cost[i][i - 1] = qi[i - 1]

    for l in range(1, n):
        for i in range(1, n - l + 1):
            j = i + l - 1
            expect_cost[i][j] = math.inf
            prob_sum[i][j] = prob_sum[i][j - 1] + pi[j] + qi[j]
            for r in range(i, j + 1):

                t = expect_cost[i][r - 1] + expect_cost[r + 1][j] + prob_sum[i][j]
                if t < expect_cost[i][j]:
                    expect_cost[i][j] = t
                    root[i][j] = r
    return root


def search_tree(root, str, start, end, s, count):
    """
    Search the tree recursively and calculate the dept (i.e. number of comparisons) and return the results
    
    params: 
    root:      generated tree
    str:       array of keys with high frequency
    start:     integer representing the starting index of the range of keys for the current subtree being searched
    end:       integer representing the ending index of the range of keys for the current subtree being searched
    s:         string representing the key being searched in the current subtree
    count:     counter of the number of depth
    """
    if start > end or end < 1:
        return None, count
    if root[start][end] == None:
        return None, count

    root_s = str[root[start][end]]

    if (not root_s) or (len(root_s) == 0) or (root_s == s):
        count += 1
        return root_s, count
    if s < root_s:
        count += 1
        return search_tree(root, str, start, root[start][end] - 1, s, count)
    count += 1

    return search_tree(root, str, root[start][end] + 1, end, s, count)


def pocet_porovnani(s, root, str):
    """
    Returns a number of comparisons for a given word
    If the given word is not found, it returns (None, depth)

    params: 
    root:      generated tree
    str:       array of keys with high frequency
    s:         string representing the key being searched in the current subtree
    """
    count = 0
    if len(s) == 0:
        return None, count
    else:
        found_key, count = search_tree(root, str, 1, len(root) - 1, s, count)

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
        key = []
        s, branch = pocet_porovnani(s, root, str)
        key.append(s)
        key.append(branch)
        branches.append(key)

    for i in branches:
        if not(i[0]):
            branches.remove(i)

    branches.sort(key=takeSecond)
    c_level = 0
    n_level = 0
    for branch in branches:

        n_level = branch[1]
        if n_level > c_level:
            c_level = n_level
            if(branch[1] == 1):
                print(f"Root {branch[1]}:")
                print(f"\t-{branch[0]}")
                continue
            print(f"Branch {branch[1]}:")
        print(f"\t-{branch[0]}")


if __name__ == "__main__":
    textArr = load("dictionary.txt")
    pi, qi, str = generate_params(textArr)
    root = generate_tree(pi, qi)
    branches(root, str)

    while True:
        print("Enter the search string (or esc to exit): ")
        inpt = input()
        if(inpt == 'esc'):
            break
        print(pocet_porovnani(inpt, root, str))
