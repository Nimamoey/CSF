import math
import numpy as np
import networkx as nx

from functools import cmp_to_key
from lattice import Lattice

#file = open('./dyn9.txt', 'w')


def weighter(weight, coloring):
    for i in range(len((coloring))):
        for j in range(i + 1):
            if coloring[i] != coloring[j]:
                weight[i][j] = weight[i][j] + 1

def weight_to_matrix(weight):
    x = np.matrix(weight)
    m = x.max()
    for i in range(len(weight)):
        for j in range(i + 1):
            if weight[i][j] == m:
                weight[i][j] = 1
                weight[j][i] = 1
            else:
                weight[i][j] = 0

def coef_fixer(partition):
    coef = partition[1]
    partition = clean_part(partition[0])

    counter = 0
    for i in range(len(partition)):
        if i == 0:
            counter = 1
        elif partition[i] == partition[i - 1]:
            counter += 1
        elif partition[i] != partition[i - 1]:
            coef *= math.factorial(counter)
            counter = 1
    coef *= math.factorial(counter)
    return [partition, coef]

def partitions_fixer(partitions):
    for i in range(len(partitions)):
        partitions[i] = coef_fixer(partitions[i])
    return partitions

def row_sum_coef(partition, n):
    ans = [0]*(n - 1)
    for part in partition:
        ans[len(clean_part(part[0])) - 2] += part[1]
    return ans

def cf_tree(n, k):
    return k*((k-1) ** (n-1))
def mat_print(mat):
    for i in range(len(mat)):
        print(" ".join(str(e) for e in mat[i]))

def is_valid_coloring(graph, vertex, color, coloring):
    for i in range(len(graph)):
        if graph[vertex][i] == 1 and coloring[i] == color:
            return False
    return True

def check_colorings(graph, colors, vertex, coloring, partitions, weight):
    n = len(graph)

    if vertex == n:
        # file.write(" ".join([str(x) for x in coloring]) + "\n")

        temp_coloring = coloring
        partitions.append(coloring_to_partition(temp_coloring))
        weighter(weight, coloring)
        return

    colors = [color for color in colors]
    colors.append(max(coloring) + 1)
    colors = list(set(colors))

    for color in colors:
        if is_valid_coloring(graph, vertex, color, coloring):
            coloring[vertex] = color
            check_colorings(graph, colors, vertex + 1, coloring, partitions, weight)
            coloring[vertex] = 0

def get_partitions(graph, num_colors):
    colors = [1]
    coloring = [0] * num_colors
    coloring[0] = 1
    partitions = []
    weight = [[0] * num_colors for i in range(num_colors)]

    check_colorings(graph, colors, 1, coloring, partitions, weight)
    return partitions

def clean_part(part):
    for i in range(len(part)):
        if part[i] == 0:
            return part[0: i]
    return part

def clean_partition(partition):
    for i in range(len(partition)):
        partition[i][0] = clean_part(partition[i][0])
    return partition

def chromatic_symmetric_function(partitions, length = 0):
    poly = ""
    if length == 0:
        length = len(partitions)

    for i in range(len(partitions)):
        temp1 = clean_part(partitions[i][0])
        if len(temp1) <= length:
            temp2 = ", ".join(str(e) for e in temp1)
            poly += str(partitions[i][1]) + "*" + "m([" + temp2 + "])" + " + "
    return poly[0: len(poly) - 2]

def sort_partitions(partitions):
    partitions = [[list(x), partitions.count(list(x))] for x in set(tuple(i) for i in partitions)]

    for i in range(0, len(partitions)):
        for j in range(i + 1, len(partitions)):
            if len(clean_part(partitions[i][0])) > len(clean_part(partitions[j][0])):
                partitions[i], partitions[j] = partitions[j], partitions[i]
            elif len(clean_part(partitions[i][0])) == len(clean_part(partitions[j][0])):
                temp = sorted([partitions[i], partitions[j]])
                partitions[i], partitions[j] = temp[1], temp[0]
    return partitions

def dic_maker(partitions):
    dic = {}

    for part in partitions:
        dic.update({tuple(clean_part(part[0])) : part[1]})
    return dic

def coloring_to_partition(coloring):
    partition = [0] * len(coloring)
    for i in coloring:
        partition[i - 1] = partition[i - 1] + 1
    partition.sort(reverse=True)
    return partition

def compare_tree_map_elements(x, y):
    x_poly = list(x[1].items())
    y_poly = list(y[1].items())
        
    n = min(len(x_poly), len(y_poly))
    
    for i in range(n):
        x_key = x_poly[i][0]
        y_key = y_poly[i][0]
        
        m = min(len(x_key), len(y_key))
        
        for j in range(m):
            if x_key[j] < y_key[j]:
                return -1
            elif x_key[j] > y_key[j]:
                return +1
        
        if len(x_key) < len(y_key):
            return -1
        elif len(x_key) > len(y_key):
            return +1
        elif x_poly[i][1] < y_poly[i][1]:
            return -1
        elif x_poly[i][1] > y_poly[i][1]:
            return +1
    return 0
    
def sort_tree_map(tree_map):
    key_func = cmp_to_key(compare_tree_map_elements)
    tree_map = sorted(tree_map, key=key_func)
    return tree_map


if __name__ == "__main__":
    n = 8
    k = 6
    
    tree_map = []
    trees = list(nx.nonisomorphic_trees(n, create='matrix'))

    for tree in trees:
        partitions = get_partitions(tree, len(tree))
        partitions = sort_partitions(partitions)
        dic = dic_maker(partitions)
        tree_map.append([tree, dic, clean_partition(partitions)])

#        for i in range(len(tree)):
#            file.write("[" + ", ".join(str(e) for e in tree[i]) + "],\n")
#        file.write(chromatic_symmetric_function(partitions) + "\n" + 15*"-" + "\n\n")
#        file.write(chromatic_symmetric_function(partitions) + "\n\n" + chromatic_symmetric_function(partitions_fixer(partitions)) + "\n\n" + 15*"-" + "\n\n")
#        print(chromatic_symmetric_function(partitions_fixer(partitions)))

        mat_print(tree)
        print(chromatic_symmetric_function(partitions, 3))

#    tree_map = sort_tree_map(tree_map)
#    
#    for x in tree_map:
#        print(x[1])
#        print()

#file.close()
