
def two_sum(array, target):
  #your code here
  lookup = {}
  for i, in range(len(array)):
      num = array[i]
      if target - num in lookup:
          return [lookup[target - num], i]
      lookup[num] = i
