import sudoku_io as gf
import random
import copy
import time

MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8

POPULATION_COUNT = 10
POPULATION_SIZE = 100

MAX_GENERATIONS = 1000


class Individual:
    def __init__(self, field):
        # self.id = random.randInt(1000,9999)
        self.currentMatrix = [row[:] for row in field]
        self.fitness = 0
        # self.population
        self._fill_empty_cells()
        self._calculate_fitness()

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


class Population:
    def __init__(self, field, size = 100):
        self.Individuals = [Individual(field) for _ in range(size)]
        self.fittest = float('+inf')
        self.avg_fitness:float = 0
        self.fitnesses = []
        self.answer = None
        self.update()

    def update(self):
        for i in self.Individuals:
            i._calculate_fitness()
        
        self.fitnesses = [] 
        for i in self.Individuals:
            self.fitnesses.append(i.fitness)
            if i.fitness == 0:
                self.answer = i

        self.fittest = min(self.fitnesses)
        self.avg_fitness = sum(self.fitnesses) / len(self.fitnesses)

class GeneticAlgorithm:

    def __init__(self, field, population_count=10, population_size=100, max_generations=1000, mutation_rate=0.2, crossover_rate=0.8):
        self.field = field
        self.population_count = population_count
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.populations = [Population(field, population_size) for _ in range(population_count)]
        self.fixed_cells = self._get_fixed_cells()

    def _get_fixed_cells(self):
        fixed_cells = []
        for row in range(9):
            for col in range(9):
                if self.field[row][col] != 0:
                    fixed_cells.append((row, col)) # если ячейка не пустая, то она фиксированная (надо допилить оптимизацию на клетки с 1 кандидатом)
        return fixed_cells

    def _crossover(self, matrix1, matrix2):
        chances = [random.randint(0,1) for i in range (9)] # какие 3х3 блоки меняем, а какие нет (нумерация 0-8)

        new_matrix1 = copy.deepcopy(matrix1) # надо оптимизировать память... но иначе не знаю как сохранять матрицы родителей для других клонирований (мб удалять их на каждом переходе к обработке другого поколения, тогда как реализовать шаги назад вперед в GUI? вопрос открыт)
        new_matrix2 = copy.deepcopy(matrix2)
        
        for row in range(9):
            for col in range(9):
                which_square = (row//3) * 3 + col//3 # логика: считаем в каком блоке находится клетка, в зависимости от значения в chancrs меняем эти блоки у матриц или нет.
                if chances[which_square] == 1:
                    new_matrix1[row][col], new_matrix2[row][col] = new_matrix2[row][col], new_matrix1[row][col]
                else:
                    continue

        return new_matrix1, new_matrix2

    def _mutatation(self, matrix):
        random_3x3 = random.randint(0, 8) # выбираем случайный блок 3х3
        row = random_3x3//3 * 3
        col = random_3x3%3 * 3

        variants = []

        for i in range(row, row+3): # собираем все нефиксированные клетки в это блоке
            for j in range(col, col+3):
                if (i,j) not in self.fixed_cells:
                    variants.append((i,j))
        
        if len(variants) >1:
            random.shuffle(variants) # перемешиваем и берем первые два элемента, их переставляем местами
            
            row_1 = variants[0][0]
            col_1 = variants[0][1]
            row_2 = variants[1][0]
            col_2 = variants[1][1]

            matrix[row_1][col_1], matrix[row_2][col_2] = matrix[row_2][col_2], matrix[row_1][col_1]


    def run(self):      
        for generation in range(self.max_generations): # в среднем обработка одного поколения занимает 0.5 сек, это значит, что 1000 поколений займет 500 секунд...

            for popul in self.populations:

                nxt_generation = []

                popul.update()
                if popul.fittest == 0:
                    print("Solution found")
                    return popul.answer.currentMatrix

                weights=[(81 - i.fitness)/(81*self.population_size - sum(popul.fitnesses)) for i in popul.Individuals] # это расчет вероятности выбора особо в кач-ве родителя (кол-во верных клеток делить на кол-во верных клеток во всей популяции)

                for i in range(self.population_size//2):
                    parents = random.choices(popul.Individuals, weights=weights, k=2) # выбираем две случ особи с учетом вероятности расчитанной выше

                    if random.random() < self.crossover_rate:
                        new_matrix1, new_matrix2 = self._crossover(parents[0].currentMatrix, parents[1].currentMatrix)
                        child1 = Individual(new_matrix1)
                        child2 = Individual(new_matrix2)
                    else:
                        child1 = Individual(copy.deepcopy(parents[0].currentMatrix))
                        child2 = Individual(copy.deepcopy(parents[1].currentMatrix))

                    if random.random() < self.mutation_rate: # вынес шанс мутации за функцию
                        self._mutatation(child1.currentMatrix) 
                    if random.random() < self.mutation_rate:
                        self._mutatation(child2.currentMatrix)

                    nxt_generation.append(child1)
                    nxt_generation.append(child2)

                popul.Individuals = nxt_generation

                

                 


# def test():
    # _, field = gf.generate_puzzle()
    # p = Individual(field.tolist())
    # for i in p.currentMatrix:
        # print(i)


if __name__ == "__main__":
    _, field = gf.generate_puzzle()
    ga = GeneticAlgorithm(field, population_count=POPULATION_COUNT, population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE)
    ga.run()

