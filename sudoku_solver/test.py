
import sudoku_io as io
import random
def break_matrix(matrix):
    for rows in range(0,9,3):
        for cols in range(0,9,3):
            for r in range(rows, rows+3):
                for c in range(cols, cols+3):
                    print(matrix[r][c], end=" ")
                print("")
            print("",end="\n\n")
def return_nth_column(matrix, column:int):
    l = set()
    for r in range(0,9):
        print(matrix[r][column], end="\n")


def return_square_fall(field, row, col):
    begin_row = row//3*3
    begin_col = col//3*3

    for x in range(begin_row, begin_row+3):
        for y in range(begin_col, begin_col+3):
            print(field[x][y], end=" ")
        print("\n")


def _check_row(field, row_num):
    
    # возвращает все числа, отсутстувующие из данной строки
    return {n for n in range(1,10) if n not in field[row_num]}
        
def _check_column(field, col_num):
    # как сверху но для столбец
    free = set()
    for rows in range(0,9):
        if field[rows][col_num] != 0:
            free.add(field[rows][col_num])
    return {n for n in range(1,10) if n not in free}

def _check_box(field, row, col):
    # Возвращает все числа, отсутствующие из данной 3х3 квадрати, дана какая нибудь точку
    free = set()
    begin_row = row//3*3
    begin_col = col//3*3

    for x in range(begin_row, begin_row+3):
        for y in range(begin_col, begin_col+3):
            if field[x][y] != 0:
                free.add(field[x][y])
    return {n for n in range(1,10) if n not in free}
def _fill_empty_cells(field): # [IN PROGRESS]: оптимизировать, чтобы не было повторов в столбцах и блоках 3x3
    filled = 0
    for rows in range(0,9,3):
       for cols in range(0,9,3):
            for r in range(rows, rows+3):
                free_row = _check_row(field, r)
                rlist = list(free_row)
                # print(f"Row: {free_row}")
                for c in range(cols, cols+3):
                    free_column = _check_column(field,c)
                    clist = list(free_column)
                    # print(f"Column: {free_column}")
                    if field[r][c] == 0:
                        free_box = _check_box(field, r, c)
                        # print(f"Box: {free_box}")
                        free = list(free_row.intersection(free_column, free_box))
                        # print(f"Total: {free}\n")
                        if not free:
                            random.shuffle(rlist)
                            field[r][c] = rlist.pop() if rlist else clist.pop()
                            # raise ValueError("bruh")
                        else:
                            random.shuffle(free)
                            field[r][c] = free[0]
                            filled+=1
    return filled

def basic_fill(field):
    filled = 0
    for row in range(9):
        empty = [n for n in range(1,10) if n not in field[row]]
        random.shuffle(empty)
        for col in range(9):
            if field[row][col] == 0:
                field[row][col] = empty.pop()
                filled+=1    
    return filled

def count_collisions(field):
    collisions = 0

    # Rows
    collisions += sum(9 - len(set(row)) for row in field)
    
    # Columns
    collisions += sum(9 - len(set(field[r][c] for r in range(9))) for c in range(9))
    
    # Boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [field[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
            collisions += 9 - len(set(box))
    
    return collisions

field = io.generate_puzzle()

print(field[1])
f = field[1].tolist()
f2 = field[1].tolist()
filled = _fill_empty_cells(f)
print(f"PRO: filled {filled} cells")
filled = basic_fill(f2)
print(f"BASIC: filled {filled} cells")
for p in f:
    print(p)
print(f"PRO: {count_collisions(f)} collisions\nBASIC: {count_collisions(f2)} collisions\n\n")


