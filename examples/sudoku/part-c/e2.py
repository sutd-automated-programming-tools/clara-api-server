import copy


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


def check_sudoku_rows(grid):
    # your solution here
    numbers = set(range(1, 10))
    for row in grid:
        copy_num = copy.copy(numbers)
        for item in row:
            int_item = int(item)
            if int_item in copy_num:
                copy_num.remove(int_item)
            else:
                return False

    return True  # <-- replace the return value


def check_sudoku_cols(grid):
    # your solution here
    numbers = set(range(1, 10))
    for col in range(9):
        copy_num = copy.copy(numbers)
        for row in range(9):
            # print(row,col)
            int_num = int(grid[row][col])
            if int_num in copy_num:
                copy_num.remove(int_num)
            else:
                return False
    return True  # <-- replace the return value


def check_sudoku_subgrids(grid):
    # your solution here
    numbers = set(range(1, 10))
    for row_sub in range(3):
        for col_sub in range(3):
            copy_num = copy.copy(numbers)
            for row in range(3):
                for col in range(3):
                    # print(row_sub * 3 + row, col_sub * 3 + col)
                    int_num = int(grid[row_sub * 3 + row][col_sub * 3 + col])
                    if int_num in copy_num:
                        copy_num.remove(int_num)
                    else:
                        return False
                    # print(int_num)
            # print('---')
    return True  # <-- replace the return value
