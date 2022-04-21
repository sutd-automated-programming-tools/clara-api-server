def add_two(list1, list2):
    str1 = ''
    str2 = ''
    if len(list1) > len(list2):
        list2 += [0] * (len(list1) - len(list2))
    else:
        list1 += [0] * (len(list2) - len(list1))
    for i in list1:
        str1 += str(i)
    str1 = str1[::-1]
    for j in list2:
        str2 += str(j)
    str2 = str2[::-1]
    i = int(str1) + int(str2)
    l = [int(x) for x in str(i)][::-1]
    return l
