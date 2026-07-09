import generate_field as gf
import random
import copy

class Individual:
    def __init__(self, field):
        # self.id = random.randInt(1000,9999)
        self.currentMatrix = [row[:] for row in field]
        self.fitness = 0
        # self.population
        self._fill_empty_cells()
        self._calculate_fitness()

    def _fill_empty_cells(self): # оптимизировать, чтобы не было повторов в столбцах и блоках 3x3
        for row in range(9):
            empty = [n for n in range(1,10) if n not in self.currentMatrix[row]]
            random.shuffle(empty) # nice hack)

            for col in range(9):
                if self.currentMatrix[row][col] == 0:
                    self.currentMatrix[row][col] = empty.pop()

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
        self.fittest = int('inf')
        self.avg_fitness:float = 0
        self._update()

    def _update(self):
        fitness = [i.fitness for i in self.Individuals]
        self.fittest = min(fitness)
        self.avg_fitness = sum(fitness) / len(fitness)


if __name__ == "__main__":
    _, field = gf.generate_puzzle()
    
