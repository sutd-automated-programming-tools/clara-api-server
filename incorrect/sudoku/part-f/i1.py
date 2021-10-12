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
        if len(row) != 9:
            result = False
            break
    return result


def check_sudoku_rows(grid):
    result = True
    for row in grid:
        for digit in range(1, 10):
            if row.count(str(digit)) != 1:
                result = False
                break
    return result


def check_sudoku_cols(grid):
    # your solution here
    counter = dict([(i, 0) for i in range(1, 10)])
    for c in range(9):
        for r in range(9):
            num = int(grid[r][c])
            if num in counter:
                counter[num] += 1
            else:
                return False
        for _, v in counter.items():
            if v != c + 1:
                return False
    return True


def check_sudoku_subgrids(grid):
    subgrid_digits = [[] for i in range(9)]
    n = 0
    for row in grid:
        index_offset = (n // 3) * 3
        subgrid_digits[index_offset + 0].extend(row[0:3])
        subgrid_digits[index_offset + 1].extend(row[3:6])
        subgrid_digits[index_offset + 2].extend(row[6:9])
        n += 1
    result = check_sudoku_rows(subgrid_digits)
    return result

#####################################################################


def string_to_grid(s):
    result = []
    for row in s.splitlines():
        result.append([val for val in row])
    return result

def check_sudoku_dimensions(grid):
    result = True
    if len(grid) != 9:
        result = False
    for row in grid:
        if len(row) != 9:
            result = False
            break
    return result

def check_sudoku_rows(grid):
    result = True
    for row in grid:
        for digit in range(1,10):
            if row.count(str(digit)) != 1:
                result = False
                break
    return result

def check_sudoku_cols(grid):
    # your solution here
    counter = dict([(i, 0) for i in range(1, 10)])
    for c in range(9):
        for r in range(9):
            num = int(grid[r][c])
            if num in counter:
                counter[num] += 1
            else:
                return False
        for _, v in counter.items():
            if v != c + 1:
                return False
    return True

def check_sudoku_subgrids(grid):
    subgrid_digits = [[] for i in range(9)]
    n = 0
    for row in grid:
        index_offset = (n//3)*3
        subgrid_digits[index_offset+0].extend(row[0:3])
        subgrid_digits[index_offset+1].extend(row[3:6])
        subgrid_digits[index_offset+2].extend(row[6:9])
        n += 1
    result = check_sudoku_rows(subgrid_digits)
    return result

def check_sudoku(s):
    grid = string_to_grid(s)
    result = (check_sudoku_dimensions(grid) + check_sudoku_rows(grid) and
             check_sudoku_cols(grid) and check_sudoku_subgrids(grid))
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

print(check_sudoku(test_case_1))