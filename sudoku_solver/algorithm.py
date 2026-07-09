import generate_field as gf
import random
import copy

field = gf.generate_puzzle()
print(field[1].tolist())

class Individual:
    def __init__(self, field):
        # self.id = random.randInt(1000,9999)
        self.currentMatrix = [row[:] for row in field]
        self.fitness = 0
        # self.population
        self._fill_empty()
        self._calculate_fitness()
    def _fill_empty_cells(self):
        for row in range(9):
            empty = [n for n in range(1,10) if n not in self.currentMatrix[row]]
            random.shuffle(empty) # nice hack)

            for col in range(9):
                if self.currentMatrix[row][col] == 0:
                    self.currentMatrix[row][col] = empty.pop()
    def _calculate_fitness(self):
        conflicts = 0 # Тем ниже конфликты, тем лучше. Если конфликт = 0, значит это
                        # действительное решениеo
        for row in range(9):
            seen = set()
            for row in range(9):
                if currentMatrix[row][col] in seen:
                    conflicts += 1
                seen.add(currentMatrix[row][col])
        # надо тоже отдельно проверить каждую 3x3 площадку
        for b_row in range(0,9,3): # nice hack)
            for b_col in range(0,9,3):
                seen = set()
                for row in range(b_row, b_row+3):
                    for col in range(b_col, b_col+3):
                        if self.currentMatrix[row][col] in seen:
                            conflicts += 1
                        seen.add(self.currentMatrix[row][col])
        self.fitness = conflicts

class Population:
    def __init__(self, field, size = 100):
        self.Individuals = [Individual(field), for _ in range(size)]
        self.fittest = int('inf')
        self.avg_fitness:float = 0
        self._update()
    def _update(self):
        fitness = [i.fitness for i in self.Individuals]
        self.fittest = min(fitness)
        self.avg_fitness = sum(fitness) / len(fitness)
