def are_same(operation1, operation2, arr_len):
    arr1 = list(range(arr_len))
    arr2 = list(range(arr_len))

    for swap in operation1:
        arr1[swap[0]], arr1[swap[1]] = arr1[swap[1]], arr1[swap[0]]
    
    for swap in operation2:
        arr2[swap[0]], arr2[swap[1]] = arr2[swap[1]], arr2[swap[0]]

    if arr1 == arr2:
        return True
    else:
        return False


def find_equivalent_operations(operation, arr_len):
    all_swaps = []
    for i in range(arr_len):
        for j in range(arr_len):
            if i != j and (i, j) not in all_swaps and (j, i) not in all_swaps:
                all_swaps.append((i, j))
    
    equal_operations = []
    for elem1 in all_swaps:
        for elem2 in all_swaps:
            current_operation = (elem1, elem2)
            if are_same(operation, current_operation, arr_len):
                equal_operations.append(current_operation)
            for elem3 in all_swaps:
                current_operation = (elem1, elem2, elem3)
                if are_same(operation, current_operation, arr_len):
                    equal_operations.append(current_operation)
                for elem4 in all_swaps:
                    current_operation = (elem1, elem2, elem3, elem4)
                    if are_same(operation, current_operation, arr_len):
                        equal_operations.append(current_operation)
                    for elem5 in all_swaps:
                        current_operation = (elem1, elem2, elem3, elem4, elem5)
                        if are_same(operation, current_operation, arr_len):
                            equal_operations.append(current_operation)
                            
                            
    
    return equal_operations
    
for elem in find_equivalent_operations([(0,2)], 4):
    print(elem)

#~ print(are_same([(0,1), (1,2), (2,3)], [(2,3), (1,2), (0,1)], 4))
