import copy
 
from classes.Population import Population
from classes.Individual import Individual
import random

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
        error_rows = []
        error_cols = []

        for i in range(9): 
            seen = []
            for j in range(9):
                val = matrix[i][j]
                if val in seen:
                    error_rows.append(i)
                    break
                seen.append(val)

        for j in range(9):
            seen = []
            for i in range(9):
                val = matrix[i][j]
                if val in seen:
                    error_cols.append(j)
                    break
                seen.append(val)

        if len(error_rows) == 0 and len(error_cols) == 0:
            return 

        is_row = True
        if len(error_rows) > 0 and len(error_cols) > 0:
            if random.random() < 0.5:
                is_row = True
            else:
                is_row = False
        elif len(error_cols) > 0:
            is_row = False

        if is_row:
            row = random.choice(error_rows)
            seen = []
            duplicates = []
            for c in range(9):
                val = matrix[row][c]
                if val in seen and val not in duplicates:
                    duplicates.append(val)
                seen.append(val)
                
            target_val = random.choice(duplicates)
            possible_cols = []
            for c in range(9):
                if matrix[row][c] == target_val:
                    possible_cols.append(c)
            col = random.choice(possible_cols)
            
        else:
            col = random.choice(error_cols)
            seen = []
            duplicates = []
            for r in range(9):
                val = matrix[r][col]
                if val in seen and val not in duplicates:
                    duplicates.append(val)
                seen.append(val)
                
            target_val = random.choice(duplicates)
            possible_rows = []
            for r in range(9):
                if matrix[r][col] == target_val:
                    possible_rows.append(r)
            row = random.choice(possible_rows)

        b_row = (row//3)* 3
        b_col = (col//3)* 3
        
        variants = []
        for i in range(b_row, b_row + 3):
            for j in range(b_col, b_col + 3):
                if (i, j) not in self.fixed_cells:
                    if i != row or j != col: 
                        variants.append((i, j))
        if len(variants) > 0:
            swap_r, swap_c = random.choice(variants)
            matrix[swap_r][swap_c], matrix[row][col] = matrix[row][col], matrix[swap_r][swap_c]

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
        best_population = min(
            self.populations,
            key=lambda population: population.fittest,
        )

        best_individual = min(
            best_population.Individuals,
            key=lambda individual: individual.fitness,
        )

        population_fitness = [
            population.fittest
            for population in self.populations
        ]

        return {
            "generation": self.current_generation,
            "best_fitness": best_population.fittest,
            "avg_fitness": (
                sum(population_fitness) / len(population_fitness)
            ),
            "population_fitness": population_fitness,
            "solved": self.solved,
            "matrix": copy.deepcopy(best_individual.currentMatrix),
        }
        

    def _tournament_selection(self, population_individuals, tournament_size=10):
            tournament = random.sample(population_individuals, tournament_size)
            return min(tournament, key=lambda x: x.fitness) 

    def step(self):
        if self.solved or self.current_generation >= self.max_generations:
            return self.get_snapshot()

        self.current_generation += 1

        for popul in self.populations:

            nxt_generation = []

            popul.update()

            start_best_fitness = popul.fittest

            if popul.fittest == 0:
                print("Solution found")
                return popul.answer.currentMatrix

            sorted_individuals = sorted(popul.Individuals, key=lambda x: x.fitness) # сортируем особей по убыванию их приспособленности

            nxt_generation.append(sorted_individuals[0]) 
            nxt_generation.append(sorted_individuals[1])

            if popul.equal_fitness_count > 50: # если за 50 поколений не было улучшения, то пересоздаем популяцию
                new_population = Population(self.field, self.population_size)
                nxt_generation += new_population.Individuals[2:]
                popul.equal_fitness_count = 0
                popul.Individuals = nxt_generation

            else:
                current_mut_rate = self.mutation_rate
                mutations_count = 1
                if popul.equal_fitness_count > 10:
                    current_mut_rate = min(0.8, self.mutation_rate*2) # повышаем шанс мутации
                    mutations_count = 2

                for i in range(self.population_size//2 - 1):
                    parent1 = self._tournament_selection(popul.Individuals)
                    parent2 = self._tournament_selection(popul.Individuals)
                    if random.random() < self.crossover_rate:
                        new_matrix1, new_matrix2 = self._crossover(parent1.currentMatrix, parent2.currentMatrix)
                        child1 = Individual(new_matrix1)
                        child2 = Individual(new_matrix2)
                    else:
                        child1 = Individual(copy.deepcopy(parent1.currentMatrix))
                        child2 = Individual(copy.deepcopy(parent2.currentMatrix))

                    if random.random() < current_mut_rate: 
                        for _ in range(mutations_count): # делаем несколько мутаций подряд
                            self._mutatation(child1.currentMatrix) 
                    if random.random() < current_mut_rate:
                        for _ in range(mutations_count):
                            self._mutatation(child2.currentMatrix)

                    nxt_generation.append(child1)
                    nxt_generation.append(child2)

                if popul.fittest >= start_best_fitness:
                    popul.equal_fitness_count += 1
                else:
                    popul.equal_fitness_count = 0

                popul.Individuals = nxt_generation
        if self.current_generation%20 ==0 and self.population_count > 1: # каждые 20 поколений делаем обмен лучшими особями между популяциями
            for i in range(self.population_count):
                best_ind = min(self.populations[i].Individuals, key=lambda x: x.fitness)
                
                next_pop_idx = (i+1)%self.population_count # берем следующую популяцию по кругу, чтобы вставить в нее лучшую особь из текущей популяции
                worst_idx = max(range(self.population_size), key=lambda j: self.populations[next_pop_idx].Individuals[j].fitness) # находим индекс худшей особи в следующей популяции
                self.populations[next_pop_idx].Individuals[worst_idx] = Individual(copy.deepcopy(best_ind.currentMatrix)) # заменяем худшую особь в следующей популяции на лучшую из текущей
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
