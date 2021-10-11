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
    counter=dict([(i,0) for i in range(1,10)])
    for c in range(9):
      for r in range(9):
        num=int(grid[r][c])
        if num in counter:
          counter+=1
        else:
          return False
      for _,v in counter.items():
        if v!=c+1:
          return False
    return True
print(check_sudoku_cols(string_to_grid(test_case_1)))
