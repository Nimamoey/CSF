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
        else :
            return -1
    return 0

def sort_partitions(list_of_partition):
    return list(sorted(list_of_partition, key = cmp_to_key(partition_comparer)))

# do not call with value 1
def expand_number(n):
    result = []
    for i in range(n - 1) :
        result.append([i + 1, n - i - 1])
    return result
        
# simple sort array
def make_standard_partiion(unsorted_partition):
    return list(sorted(unsorted_partition))

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
         
def find_lowest_common_ancestor(partition1, partition2):
    return find_lowest_common_ancestor_util([make_standard_partiion(partition1)], [make_standard_partiion(partition2)])
         
def find_lowest_common_ancestor_util(list_of_partition1, list_of_partition2):
    if len(list_of_partition1[0]) > len(list_of_partition2[0]) :
        return find_lowest_common_ancestor_util(list_of_partition2, list_of_partition1)
    while len(list_of_partition1[0]) < len(list_of_partition2[0]):
        list_of_partition1 = expander_list(list_of_partition1)
    return find_lowest_common_ancestor_with_same_size(list_of_partition1, list_of_partition2)

def find_lowest_common_ancestor_with_same_size(list_of_partition1, list_of_partition2):
    while find_common_element(list_of_partition1, list_of_partition2) == None:
        list_of_partition1 = expander_list(list_of_partition1)
        list_of_partition2 = expander_list(list_of_partition2)
    return find_common_element(list_of_partition1, list_of_partition2)

def find_common_element(list_of_partition1, list_of_partition2):
    for e in list_of_partition1:
        if e in list_of_partition2:
            return e
    return None

print (find_lowest_common_ancestor([4 , 4 , 3] , [10, 1]))
