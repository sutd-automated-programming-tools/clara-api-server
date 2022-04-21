def add_two(list1, list2):
    f, s = (list1, list2) if len(list1) > len(list2) else (list2, list1)
    for i in range(len(f)):
        f[i] += s[i] if i < len(s) else 0
        if f[i] >= 10:
            f[i] %= 10
            if i < len(f) - 1:
                f[i + 1] += 1
            else:
                f += [1]
    return f
