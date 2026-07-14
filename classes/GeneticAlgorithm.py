import copy
 
from classes.Population import Population
from classes.Individual import Individual
import random

from sudoku_solver.sudoku_io import generate_puzzle as gf

class GeneticAlgorithm:

    def __init__(self, field, population_count=10, population_size=100, max_generations=1000, mutation_rate=0.2, crossover_rate=0.8):
        self.field = copy.deepcopy(field)
        self.current_generation = 0
        self.solved = False
        self.solution = None
        self.population_count = population_count
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.populations = [
            Population(copy.deepcopy(self.field), population_size)
            for _ in range(population_count)
        ]   
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

    def get_generation_stats(self):
        best_individual = None
        best_fitness = float("inf")
        all_fitnesses = []

        for popul in self.populations:
            popul.update()

            for individual in popul.Individuals:
                fitness = individual.fitness
                all_fitnesses.append(fitness)

                if fitness < best_fitness:
                    best_fitness = fitness
                    best_individual = individual

        if not all_fitnesses:
            raise ValueError("Нет особей для расчета fitness")

        avg_fitness = sum(all_fitnesses) / len(all_fitnesses)

        return best_individual, best_fitness, avg_fitness
    
    def get_snapshot(self):
        best_individual, best_fitness, avg_fitness = self.get_generation_stats()

        return {
            "generation": self.current_generation,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness,
            "matrix": copy.deepcopy(best_individual.currentMatrix),
            "solved": best_fitness == 0,
        }
    
    def step(self):
        if self.solved or (self.current_generation >= self.max_generations):
            return self.get_snapshot()

        self.current_generation += 1

        for popul in self.populations:

            nxt_generation = []

            popul.update()

            start_best_fitness = popul.fittest

            if popul.fittest == 0:
                print("Solution found")
                return popul.answer.currentMatrix

            weights=[(81 - i.fitness)/(81*self.population_size - sum(popul.fitnesses)) for i in popul.Individuals] # это расчет вероятности выбора особо в кач-ве родителя (кол-во верных клеток делить на кол-во верных клеток во всей популяции)

            sorted_individuals = sorted(popul.Individuals, key=lambda x: x.fitness) # сортируем особей по убыванию их приспособленности

            nxt_generation.append(sorted_individuals[0]) 
            nxt_generation.append(sorted_individuals[1])
            nxt_generation.append(sorted_individuals[2])
            nxt_generation.append(sorted_individuals[3]) 

            if popul.equal_fitness_count > 50: # если за 50 поколений не было улучшения, то пересоздаем популяцию
                new_population = Population(self.field, self.population_size)
                nxt_generation += new_population.Individuals[4:]
                popul.equal_fitness_count = 0
                popul.Individuals = nxt_generation

            else:

                for i in range(self.population_size//2 - 2):
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

                if popul.fittest <= start_best_fitness:
                    popul.equal_fitness_count += 1
                else:
                    popul.equal_fitness_count = 0

                popul.Individuals = nxt_generation
        snapshot = self.get_snapshot()

        if snapshot["solved"]:
            self.solved = True
            self.solution = copy.deepcopy(snapshot["matrix"])

        return snapshot

    def run(self):
        snapshot = self.get_snapshot()

        while not self.solved and self.current_generation < self.max_generations:
            snapshot = self.step()

            if snapshot["solved"]:
                return snapshot

        return snapshot

MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8

POPULATION_COUNT = 10
POPULATION_SIZE = 100

MAX_GENERATIONS = 1000          

if __name__ == "__main__":
    _, field = gf()
    ga = GeneticAlgorithm(field, population_count=POPULATION_COUNT, population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE)
    ga.run()
    
