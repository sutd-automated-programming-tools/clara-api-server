def search_position(array, target):
  i=0
  while i<len(array):
    if array[i]>=target:
      return i
    i+=1
  return i