def string_to_grid(s):
    result = []
    for row in s.splitlines():
        result.append([val for val in row])
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


def check_sudoku_dimensions(grid):
    result = True
    if len(grid) != 9:
        result = False
    for row in grid:
        if len(row) != 11:
            result = False
            break
    return result


def check_sudoku_rows(grid):
    result = True
    return result


print(check_sudoku_dimensions(string_to_grid(test_case_1)))
