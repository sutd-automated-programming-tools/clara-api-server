def search_position(array, target):
    for i in range(len(array)):
      if target<=array[i]:
        return i
    return i+1