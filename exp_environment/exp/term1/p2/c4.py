
def add_two(list1, list2):
    n_min = min(len(list1),len(list2))
    n_max = max(len(list1),len(list2))
    output = []
    carry = 0
    for index in range(n_min):
        item1 = list1[index] 
        item2 = list2[index]
        total = item1 + item2 + carry
        new = total % 10
        carry = total // 10
        output.append(new)  
        
    start = index + 1
    if len(list1) == n_max:
        long = list1
    else:
        long = list2
        
    for index in range(start,n_max):
        item = long[index]
        total = item + carry
        new = total % 10
        carry = total // 10
        output.append(new)  
    if carry != 0:
        output.append(carry)
    return output
