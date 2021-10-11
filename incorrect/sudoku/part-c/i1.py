# Sample solution

def check_sudoku_rows(grid):
    result = True
    for row in grid:
        for digit in range(1,10):
            if row.count(str(digit)) != 1:
                result = False
                break
    return result

print(check_sudoku_rows(string_to_grid(test_case_1)))