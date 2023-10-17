from utils import generate_random_trees_list
import random


class GeneticProgramming:
    def __init__(self, dataset, population_size, max_depth, max_generations, terminal_set, function_set, early_stop, crossover_rate=0.7):
        self.dataset = dataset
        self.population_size = population_size
        self.max_depth = max_depth
        self.max_generations = max_generations
        self.terminal_set = terminal_set
        self.function_set = function_set

        self.population = generate_random_trees_list(
            population_size, max_depth, terminal_set, function_set, early_stop)
        print(self.population)

        self.fitness = [(tree, self.evaluate(tree))
                        for tree in self.population]

    def select_fit_nodes(self, tournament_ratio=20):
        selected_for_tournament = random.sample(
            self.fitness, self.population_size//tournament_ratio)
        return max(selected_for_tournament, key=lambda x: x[1])[0]

    def reproduce(self, parents):
        new_population = []
        for i in range(0, self.population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = parent1.crossover(parent2)
            new_population.extend([child1, child2])
        for child in new_population:
            if random.random() < 0.1:  # 10% mutation rate
                child.mutate()
        return new_population

    def evaluate(self, tree):
        error = 0
        for x, y in self.dataset:
            prediction = tree.evaluate(tree.root, x)
            error += (prediction - y) ** 2
        return error / len(self.dataset)

    def terminate(self, current_generation, satisfactory_fitness):
        if current_generation >= self.max_generations:
            return True
        best_fitness = min(self.fitness, key=lambda x: x[1])[1]
        if best_fitness <= satisfactory_fitness:
            return True

    def genetic_algorithm(self, num_run, crossover_prob):
        for _ in range(num_run):
            for _ in range(self.max_generations):
                new_population = []
                for i in range(self.population_size):
                    rand = random.random()

                    # Crossover
                    if rand < crossover_prob:
                        parent1 = self.select_fit_nodes(self.population)
                        parent2 = self.select_fit_nodes(self.population)
                        offspring = parent1.crossover(parent1, parent2)
                        new_population.append(offspring)

                    # Mutation
                    else:
                        individual = self.select_fit_nodes(self.population)
                        mutant = individual.mutate(individual)
                        new_population.append(mutant)

                # Replace the old population with the new population
                self.population = new_population[:]

                # Check termination criterion for the run (assuming it's a function)
                if self.terminate(self.population):
                    break
        return self.population
