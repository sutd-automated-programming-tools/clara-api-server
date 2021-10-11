def string_to_grid(s):
    # your solution here
    output = []
    lines = s.split()
    for line in lines:
        output_row = []
        for char in line:
            output_row.append(char)
        output.append(output_row)
    return output  # <-- replace the return value


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
    # your solution here
    row = len(grid)
    if row != 9:
        return False
    for row in grid:
        if len(row) != 9:
            return False
    return True  # <-- replace the return value


print(check_sudoku_dimensions(string_to_grid(test_case_1)))
