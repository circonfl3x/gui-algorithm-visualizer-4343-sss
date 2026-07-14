import random
class Individual:
    def __init__(self, field):
        # self.id = random.randInt(1000,9999)
        self.currentMatrix = [row[:] for row in field]
        self.fitness = 0
        # self.population
        self._fill_empty_cells()
        self._calculate_fitness()

    def _fill_empty_cells_old(self): # оптимизировать, чтобы не было повторов в столбцах и блоках 3x3
        for row in range(9):
            empty = [n for n in range(1,10) if n not in self.currentMatrix[row]]
            random.shuffle(empty) # nice hack)

            for col in range(9):
                if self.currentMatrix[row][col] == 0:
                    self.currentMatrix[row][col] = empty.pop()
    def _check_row(self, row_num):
        # возвращает все числа, отсутстувующие из данной строки
        return {n for n in range(1,10) if n not in self.currentMatrix[row_num]}
        
    def _check_column(self, col_num):
        # как сверху но для столбец
        free = set()
        for rows in range(0,9):
            if self.currentMatrix[rows][col_num] != 0:
                free.add(self.currentMatrix[rows][col_num])
        return {n for n in range(1,10) if n not in free}

    def _check_box(self, row, col):
        # Возвращает все числа, отсутствующие из данной 3х3 квадрати, дана какая нибудь точку
        free = set()
        begin_row = row//3*3
        begin_col = col//3*3

        for x in range(begin_row, begin_row+3):
            for y in range(begin_col, begin_col+3):
                if self.currentMatrix[x][y] != 0:
                    free.add(self.currentMatrix[x][y])
        return {n for n in range(1,10) if n not in free}
    
    def _fill_empty_cells(self): # DONE: оптимизировать, чтобы не было повторов в блоках 3x3
        for b_row in range(3):
            for b_col in range(3):
                existing_numbers = set()
                for i in range(3):
                    for j in range(3):
                        val = self.currentMatrix[b_row * 3+i][b_col *3+j]
                        if val != 0:
                            existing_numbers.add(val)
                missing_numbers = list(set(range(1, 10)) - existing_numbers)
                random.shuffle(missing_numbers)
                for i in range(3):
                    for j in range(3):
                        if self.currentMatrix[b_row * 3+i][b_col * 3+j] == 0:
                            self.currentMatrix[b_row * 3+i][b_col * 3+j] = missing_numbers.pop()
    
    def _calculate_fitness(self):
        conflicts = 0 
        for i in range(9):
            row_seen = set()
            col_seen = set()
            for j in range(9):
                row_val = self.currentMatrix[i][j]
                if row_val in row_seen:
                    conflicts += 1
                else:
                    row_seen.add(row_val)       
                col_val = self.currentMatrix[j][i]
                if col_val in col_seen:
                    conflicts += 1
                else:
                    col_seen.add(col_val)
                    
        self.fitness = conflicts