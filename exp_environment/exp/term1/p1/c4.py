def search_position(array,target):
    #your code here
    index = 0
    for item in array:
        if target < item:
            return index
        elif target == item:
            return index
        elif target > item and (index == len(array)-1 or target < array[index + 1]):
            return index + 1
        else:
            index += 1