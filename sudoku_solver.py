from itertools import product

def sudoku_validator(sudoku, count_blank_spaces=True):
    """
    To be able to validate the sudoku what we are going to do is to take each clumn and wach row and compare the elemenst within them to see if the repeat.

    What I mean by that is that for example, we are going to take first row and the first column 
    [[row = 0, column = 0]] with this in mind we are going to perfomn a while loop until we have checked all the elements in the given row and in the given column, if the numbers do not repeat we are good to go otherwise we just return False meaning that it is not a validate sudoku.
    """

    for row in range(len(sudoku)):
        for column in range(len(sudoku[row])):
            if not validate_row_and_column(row, column, sudoku, count_blank_spaces):
                return False

    return True


def validate_row_and_column(x, y, sudoku, count_blank_spaces):
    row = []
    column = []

    for n in range(len(sudoku)):
        if sudoku[n][y] in row or sudoku[x][n] in column:
            return False
        
        if count_blank_spaces:
            if sudoku[n][y] == 0 or sudoku[x][n] == 0:
                return False
        
        if sudoku[n][y] != 0:
            row.append(sudoku[n][y])

        if sudoku[x][n] != 0:
            column.append(sudoku[x][n])

        start_x_square = (x // 3) * 3
        start_y_square = (y // 3) * 3

        numbers_in_square = []

        for _x in range(3):
            for _y in range(3):
                if sudoku[start_x_square + _x][start_y_square + _y] in numbers_in_square:
                    return False
                
                if sudoku[start_x_square + _x][start_y_square + _y] != 0:
                    numbers_in_square.append(sudoku[start_x_square + _x][start_y_square + _y])
                

    return True
    

def sudoku_solver(size, sudoku):
    ROW, COlUMN = size
    N = ROW * COlUMN

    X = (
        [('rc', rc) for rc in product(range(N), range(N))] +
        [('rn', rn) for rn in product(range(N), range(1, N + 1))] +
        [('cn', cn) for cn in product(range(N), range(1, N + 1))] +
        [('bn', bn) for bn in product(range(N), range(1, N + 1))
        ])
    
    Y = dict()

    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // ROW) * ROW + (c // COlUMN) # box number
        Y[(r, c, n)] = [
            ('rc', (r, c)),
            ('rn', (r, n)),
            ('cn', (c, n)),
            ('bn', (b, n))
        ]
    
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(sudoku):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            sudoku[r][c] = n
        
        try:
            yield sudoku
        finally:
            pass

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    
    return X, Y


def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            columns = select(X, Y, r)
            for solu in solve(X, Y, solution):
                yield solu
            deselect(X, Y, r, columns)
            solution.pop()


def select(X, Y, r):
    columns = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        columns.append(X.pop(j))
    return columns


def deselect(X, Y, r, columns):
    for j in reversed(Y[r]):
        X[j] = columns.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)