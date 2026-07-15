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
            possible_cols = [
                c
                for c in range(9)
                if (
                    matrix[row][c] == target_val
                    and (row, c) not in self.fixed_cells
                )
            ]

            if not possible_cols:
                return

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
            possible_rows = [
                r
                for r in range(9)
                if (
                    matrix[r][col] == target_val
                    and (r, col) not in self.fixed_cells
                )
            ]

            if not possible_rows:
                return

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

    def get_snapshot(self):
        best_individuals = []

        for population in self.populations:
            if not population.Individuals:
                raise ValueError("В популяции отсутствуют особи")

            best_in_population = min(
                population.Individuals,
                key=lambda individual: individual.fitness,
            )

            best_individuals.append(best_in_population)
            population.fittest = best_in_population.fitness

        population_fitness = [
            individual.fitness
            for individual in best_individuals
        ]

        best_individual = min(
            best_individuals,
            key=lambda individual: individual.fitness,
        )

        best_fitness = best_individual.fitness

        if best_fitness == 0:
            self.solved = True
            self.solution = copy.deepcopy(
                best_individual.currentMatrix
            )

        return {
            "generation": self.current_generation,
            "best_fitness": best_fitness,
            "avg_fitness": (
                sum(population_fitness) / len(population_fitness)
            ),
            "population_fitness": population_fitness,
            "solved": self.solved,
            "matrix": copy.deepcopy(best_individual.currentMatrix),
        }
        

    def _tournament_selection(
        self,
        population_individuals,
        tournament_size=10,
    ):
        if not population_individuals:
            raise ValueError("Нельзя выбрать особь из пустой популяции")

        actual_size = min(
            tournament_size,
            len(population_individuals),
        )

        tournament = random.sample(
            population_individuals,
            actual_size,
        )

        return min(
            tournament,
            key=lambda individual: individual.fitness,
        )
    
    def step(self):
        if self.solved or self.current_generation >= self.max_generations:
            return self.get_snapshot()

        self.current_generation += 1

        for population in self.populations:
            population.update()

            if population.fittest == 0:
                print("Solution found")
                return self.get_snapshot()

            start_best_fitness = population.fittest

            sorted_individuals = sorted(
                population.Individuals,
                key=lambda individual: individual.fitness,
            )

            # Сохраняем двух лучших особей — элитизм
            next_generation = [
                Individual(copy.deepcopy(sorted_individuals[0].currentMatrix)),
                Individual(copy.deepcopy(sorted_individuals[1].currentMatrix)),
            ]

            # Если улучшений долго нет — пересоздаём популяцию,
            # сохраняя двух лучших особей
            if population.equal_fitness_count >= 50:
                new_population = Population(
                    copy.deepcopy(self.field),
                    self.population_size,
                )

                individuals_needed = (
                    self.population_size - len(next_generation)
                )

                next_generation.extend(
                    new_population.Individuals[:individuals_needed]
                )

                population.equal_fitness_count = 0

            else:
                current_mutation_rate = self.mutation_rate
                mutations_count = 1

                if population.equal_fitness_count > 10:
                    current_mutation_rate = min(
                        0.8,
                        self.mutation_rate * 2,
                    )
                    mutations_count = 2

                while len(next_generation) < self.population_size:
                    parent1 = self._tournament_selection(
                        population.Individuals
                    )
                    parent2 = self._tournament_selection(
                        population.Individuals
                    )

                    if random.random() < self.crossover_rate:
                        matrix1, matrix2 = self._crossover(
                            parent1.currentMatrix,
                            parent2.currentMatrix,
                        )
                    else:
                        matrix1 = copy.deepcopy(parent1.currentMatrix)
                        matrix2 = copy.deepcopy(parent2.currentMatrix)

                    # Мутируем матрицы до создания Individual,
                    # чтобы fitness соответствовал матрице
                    if random.random() < current_mutation_rate:
                        for _ in range(mutations_count):
                            self._mutatation(matrix1)

                    if random.random() < current_mutation_rate:
                        for _ in range(mutations_count):
                            self._mutatation(matrix2)

                    next_generation.append(Individual(matrix1))

                    if len(next_generation) < self.population_size:
                        next_generation.append(Individual(matrix2))

                new_best_fitness = min(
                    individual.fitness
                    for individual in next_generation
                )

                if new_best_fitness < start_best_fitness:
                    population.equal_fitness_count = 0
                else:
                    population.equal_fitness_count += 1

            population.Individuals = next_generation

        # Каждые 20 поколений переносим лучшую особь
        # каждой популяции в следующую
        if (
            self.current_generation % 20 == 0
            and self.population_count > 1
        ):
            migrants = [
                min(
                    population.Individuals,
                    key=lambda individual: individual.fitness,
                )
                for population in self.populations
            ]

            for population_index, migrant in enumerate(migrants):
                next_population_index = (
                    population_index + 1
                ) % self.population_count

                next_population = self.populations[
                    next_population_index
                ]

                worst_index = max(
                    range(len(next_population.Individuals)),
                    key=lambda index: (
                        next_population.Individuals[index].fitness
                    ),
                )

                next_population.Individuals[worst_index] = Individual(
                    copy.deepcopy(migrant.currentMatrix)
                )

        return self.get_snapshot()

    def run(self):
        snapshot = self.get_snapshot()

        while not self.solved and self.current_generation < self.max_generations:
            snapshot = self.step()

            if snapshot["solved"]:
                return snapshot

        return snapshot    
