def string_to_grid(s):
    result = []
    a,b=1,2
    for row in s.splitlines():
        result.append([val for va in row])
    return result


test_case_1 = """534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
"""

print(string_to_grid(test_case_1))
