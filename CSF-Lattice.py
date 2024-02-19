from functools import cmp_to_key


def unique_partition(list_of_partition):
    result = [list_of_partition[0]]
    for partition in list_of_partition:
        if partition_comparer(partition, result[-1]) == 0:
            continue
        result.append(partition)
    return result

def partition_comparer(partition1, partition2):
    for i, x in enumerate(partition1):
        y = partition2[i]
        if x == y:
            continue
        if x < y:
            return 1
        else:
            return -1
    return 0

def sort_partitions(list_of_partition):
    return list(sorted(list_of_partition, key = cmp_to_key(partition_comparer)))

# simple sort array
def make_standard_partiion(unsorted_partition):
    return list(sorted(unsorted_partition))

def find_common_element(list_of_partition1, list_of_partition2):
    for e in list_of_partition1:
        if e in list_of_partition2:
            return e
    return None

""" HIGHEST COMMON CHILD """

# do not call with value 1
def expand_number(n):
    result = []
    for i in range(n - 1) :
        result.append([i + 1, n - i - 1])
    return result

def expander(partition):
    results = []
    for i, e in enumerate(partition):
        if e == 1:
            continue
        for expanded in expand_number(e):
            results.append(make_standard_partiion(partition[:i] + expanded + partition[i + 1:]))
    results = sort_partitions(results)
    results = unique_partition(results)
    return results

def expander_list(list_of_partition):
    result = []
    for partition in list_of_partition:
        result = result + expander(partition)
    result = sort_partitions(result)
    result = unique_partition(result)
    return result
         
def find_highest_common_child(partition1, partition2):
    return find_highest_common_child_util([make_standard_partiion(partition1)], [make_standard_partiion(partition2)])
         
def find_highest_common_child_util(list_of_partition1, list_of_partition2):
    if len(list_of_partition1[0]) > len(list_of_partition2[0]) :
        return find_highest_common_child_util(list_of_partition2, list_of_partition1)
    while len(list_of_partition1[0]) < len(list_of_partition2[0]):
        list_of_partition1 = expander_list(list_of_partition1)
    return find_highest_common_child_with_same_size(list_of_partition1, list_of_partition2)

def find_highest_common_child_with_same_size(list_of_partition1, list_of_partition2):
    while find_common_element(list_of_partition1, list_of_partition2) == None:
        list_of_partition1 = expander_list(list_of_partition1)
        list_of_partition2 = expander_list(list_of_partition2)
    return find_common_element(list_of_partition1, list_of_partition2)

""" LOWEST COMMON ANCESTOR """

def shrinker(partition):
    results = []
    for i, e in enumerate(partition):
        for j, f in enumerate(partition):
            if i >= j:
                continue
            results.append(make_standard_partiion(partition[:i] + partition[i + 1:j] + partition[j + 1:] + [e + f]))
    results = sort_partitions(results)
    results = unique_partition(results)
    return results

def shrinker_list(list_of_partition):
    result = []
    for partition in list_of_partition:
        result = result + shrinker(partition)
    result = sort_partitions(result)
    result = unique_partition(result)
    return result
         
def find_lowest_common_ancestor(partition1, partition2):
    return find_lowest_common_ancestor_util([make_standard_partiion(partition1)], [make_standard_partiion(partition2)])
         
def find_lowest_common_ancestor_util(list_of_partition1, list_of_partition2):
    if len(list_of_partition1[0]) < len(list_of_partition2[0]) :
        return find_lowest_common_ancestor_util(list_of_partition2, list_of_partition1)
    while len(list_of_partition1[0]) > len(list_of_partition2[0]):
        list_of_partition1 = shrinker_list(list_of_partition1)
    return find_lowest_common_ancestor_with_same_size(list_of_partition1, list_of_partition2)

def find_lowest_common_ancestor_with_same_size(list_of_partition1, list_of_partition2):
    while find_common_element(list_of_partition1, list_of_partition2) == None:
        list_of_partition1 = shrinker_list(list_of_partition1)
        list_of_partition2 = shrinker_list(list_of_partition2)
    return find_common_element(list_of_partition1, list_of_partition2)

""" ANCESTOR/CHILD LEVEL EQUAL """

def find_ancestor_level_equal(partition1, partition2):
    return find_ancestor_level_equal_util([make_standard_partiion(partition1)], [make_standard_partiion(partition2)])
    
def find_ancestor_level_equal_util(list_of_partition1, list_of_partition2):
    if len(list_of_partition1[0]) < len(list_of_partition2[0]) :
        return find_ancestor_level_equal_util(list_of_partition2, list_of_partition1)
    while len(list_of_partition1[0]) > len(list_of_partition2[0]):
        list_of_partition1 = shrinker_list(list_of_partition1)
    return find_level_equal_same_size(list_of_partition1, list_of_partition2, -1)

def find_child_level_equal(partition1, partition2):
    return find_child_level_equal_util([make_standard_partiion(partition1)], [make_standard_partiion(partition2)])

def find_child_level_equal_util(list_of_partition1, list_of_partition2):
    if len(list_of_partition1[0]) > len(list_of_partition2[0]) :
        return find_child_level_equal_util(list_of_partition2, list_of_partition1)
    while len(list_of_partition1[0]) < len(list_of_partition2[0]):
        list_of_partition1 = expander_list(list_of_partition1)
    return find_level_equal_same_size(list_of_partition1, list_of_partition2, +1)

def find_level_equal_same_size(list_of_partition1, list_of_partition2, constraint):
    selected_level_equal = list_of_partition1[0]
    for partition in list_of_partition1:
        if partition_comparer(partition, selected_level_equal) == constraint:
            selected_level_equal = partition
    for partition in list_of_partition2:
        if partition_comparer(partition, selected_level_equal) == constraint:
            selected_level_equal = partition
    return selected_level_equal

a = [8]
b = [5, 2, 1]

print("ANCESTOR LEVEL EQUAL:")
print(find_ancestor_level_equal(a, b))

print("\nCHILD LEVEL EQUAL:")
print(find_child_level_equal(a, b))

print("\nHIGHEST COMMON CHILD:")
print(find_highest_common_child(a, b))

print("\nLOWEST COMMON ANCESTOR:")
print(find_lowest_common_ancestor(a, b))
