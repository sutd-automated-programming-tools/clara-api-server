
def two_sum(array, target):
  #your code here
  for index1 in range(len(array)):
    for index2 in range(index1 + 1, len(array)):
      item1 = array[index1]
      item2 = array[index2]
      if index1 != index2 and target == (item1 + item2):
        return ([index1, index2])
