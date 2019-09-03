def bubbleSort(array):
    opcount = 0
    for i in range(len(array) - 1):
        for j in range(len(array) - 1):
            nochangeneeded = 1
            print(array[j], array[j+1])
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                opcount += 1
                nochangeneeded = 0
        if nochangeneeded:
            break
    return array, opcount


print(bubbleSort(list(reversed([x for x in range(1, 10)]))))
