def search_position(array, target):
    i = 0
    while i < len(array):
        if target >= array[i]:
            return i
        i += 1
    return i
