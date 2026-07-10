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
    def _fill_empty_cells(self): # DONE: оптимизировать, чтобы не было повторов в столбцах и блоках 3x3

        for rows in range(0,9,3):
            for cols in range(0,9,3):
                for r in range(rows, rows+3):
                    free_row = self._check_row(r)
                    rlist = list(free_row)
                    for c in range(cols, cols+3):
                        free_column = self._check_column(c)
                        clist = list(free_column)
                        if self.currentMatrix[r][c] == 0:
                            free_box = self._check_box(r, c)
                            free = list(free_row.intersection(free_column, free_box))
                            if not free:
                                # raise ValueError("No common elements so matrix couldn't be filled!")
                                random.shuffle(rlist)
                                random.shuffle(clist)
                                self.currentMatrix[r][c] = rlist.pop() if rlist else clist.pop()
                            else:
                                random.shuffle(free)
                                self.currentMatrix[r][c] = free[0]
    
    def _calculate_fitness(self):
        conflicts = 0 # Тем ниже конфликты, тем лучше. Если конфликт = 0, значит это
                        # действительное решение
        for row in range(9):
            seen_row = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}

            for col in range(9):
                seen_row[str(self.currentMatrix[row][col])] = seen_row.get(str(self.currentMatrix[row][col]), 0) + 1
            
            for count in seen_row.values():
                if count > 1:
                    conflicts += count  # число встретилось не один раз => каждое число конфилктное

        for col in range(9):
            seen_col = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}

            for row in range(9):
                seen_col[str(self.currentMatrix[row][col])] = seen_col.get(str(self.currentMatrix[row][col]), 0) + 1

            for count in seen_col.values():
                if count > 1:
                    conflicts += count  # число встретилось не один раз => каждое число конфилктное

        # надо тоже отдельно проверить каждую 3x3 площадку
        for b_row in range(3):
            for b_col in range(3):
                seen_col = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
                for row in range(b_row*3, (b_row+1)*3):
                    for col in range(b_col*3, (b_col+1)*3):
                        seen_col[str(self.currentMatrix[row][col])] = seen_col.get(str(self.currentMatrix[row][col]), 0) + 1

                for count in seen_col.values():
                    if count > 1:
                        conflicts += count  # число встретилось не один раз => каждое число конфилктное
        
        self.fitness = conflicts
