from classes.Individual import Individual
class Population:
    def __init__(self, field, size = 100):
        self.Individuals = [Individual(field) for _ in range(size)]
        self.fittest = float('+inf')
        self.avg_fitness:float = 0
        self.fitnesses = []
        self.answer = None
        self.equal_fitness_count = 0
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
