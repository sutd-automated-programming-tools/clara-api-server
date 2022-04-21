def add_two(list1, list2):
    list3 = []
    if len(list1) > len(list2):
        list3 += [0] * len(list1)
    else:
        list3 += [0] * len(list2)
    for i in range(len(list1)):
        list3[i] += list1[i]
    for i in range(len(list3)):
        list3[i] += list2[i] if i < len(list2) else 0
        if list3[i] >= 10:
            list3[i] %= 10
            if i < len(list3) - 1:
                list3[i + 1] += 1
            else:
                list3 += [1]

    return list3
