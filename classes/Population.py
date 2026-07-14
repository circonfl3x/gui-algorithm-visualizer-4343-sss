from classes.Individual import Individual
import statistics
class Population:
    def __init__(self, field, size = 100, history=50, variance_limit=2):
        self.Individuals = [Individual(field) for _ in range(size)]
        self.fittest = float('+inf')
        self.avg_fitness:float = 0
        self.fitnesses = []
        self.history_fittest = []
        self.history_size = history
        self.answer = None
        self.increase_mutate = False
        self.variance_limit = variance_limit
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
        if len(self.history_fittest) < self.history_size :
            self.history_fittest.append(self.fittest)
        else:
            print(statistics.stdev(self.history_fittest))
            if statistics.stdev(self.history_fittest) < self.variance_limit:
                self.increase_mutate = True
            self.history_fittest.pop(0)
            self.history_fittest.append(self.fittest)
        self.avg_fitness = sum(self.fitnesses) / len(self.fitnesses)
        if self.increase_mutate:
            self.increase_mutate = False
            return False
