from utils import generate_random_trees_list, train_test_split
import random


class GeneticProgramming:
    def __init__(self, dataset, population_size, max_depth, max_generations, terminal_set, function_set, early_stop, crossover_rate, migration_rate, migration_size):
        self.dataset = dataset
        self.population_size = population_size
        self.max_depth = max_depth
        self.max_generations = max_generations
        self.terminal_set = terminal_set
        self.function_set = function_set
        self.early_stop = early_stop
        self.migration_rate = migration_rate
        self.migration_size = migration_size
        self.crossover_rate = crossover_rate

    def generate_fitness(self):
        fitness = []
        for tree in self.population:
            fitness.append((tree, self.evaluate(tree)))
        return fitness

    def select_fit_nodes(self, tournament_ratio=100):
        selected_for_tournament = random.sample(
            self.fitness, self.population_size//tournament_ratio)
        return min(selected_for_tournament, key=lambda x: x[1])[0]

    def evaluate(self, tree, regularization_lambda=100):
        total_error = 0
        n = len(self.dataset)
        for (x1, x2, x3), y in self.dataset:
            prediction = tree.evaluate_tree(tree.root, x1, x2, x3)
            error = (prediction - y)**2  # Squaring the error
            total_error += error
        mse = total_error / n
        depth_penalty = regularization_lambda * tree.get_depth()
        return mse + depth_penalty

    def evaluate_test_set(self, tree, test_set):
        total_error = 0
        n = len(test_set)
        for (x1, x2, x3), y in test_set:
            prediction = tree.evaluate_tree(tree.root, x1, x2, x3)
            error = (prediction - y)**2  # Squaring the error
            total_error += error
        mse = total_error / n
        return mse

    def terminate(self, satisfactory_fitness=1):  # Adjust this value as needed
        best_fitness = min(self.fitness, key=lambda x: x[1])[1]
        return best_fitness <= satisfactory_fitness

    def genetic_algorithm(self, num_run, crossover_rate, migration_rate):
        # Split the dataset into train and test sets
        train_set, test_set = train_test_split(self.dataset)
        self.dataset = train_set  # Set the dataset to the training set for evaluation

        best_tree = None
        best_tree_error = float('inf')

        for _ in range(num_run):
            self.population = generate_random_trees_list(
                self.population_size, self.max_depth, self.terminal_set, self.function_set, self.early_stop)
            self.fitness = self.generate_fitness()
            for _ in range(self.max_generations):
                new_population = []
                best_tree = min(self.fitness, key=lambda x: x[1])[0]
                new_population.append(best_tree)
                while len(new_population) < self.population_size:
                    rand = random.random()

                    # Crossover
                    if rand < crossover_rate:
                        parent1 = self.select_fit_nodes()
                        parent2 = self.select_fit_nodes()
                        offspring1, offspring2 = parent1.crossover(parent2)
                        new_population.append(parent1)
                        new_population.append(parent2)
                        new_population.append(offspring1)
                        new_population.append(offspring2)
                    elif rand < crossover_rate+migration_rate:
                        migrations = generate_random_trees_list(
                            self.migration_size, self.max_depth, self.terminal_set, self.function_set, self.early_stop)
                        new_population += migrations
                        
                    # Mutation
                    else:
                        individual = self.select_fit_nodes()
                        mutant = individual.mutate()
                        new_population.append(individual)
                        new_population.append(mutant)
                # Replace the old population with the new population
                self.population = new_population
                self.fitness = self.generate_fitness()
                # Check termination criterion for the run
                if self.terminate():
                    break
                with open("results.txt", 'a') as file:
                    file.write("The best tree is: " + str(min(
                    self.fitness, key=lambda x: x[1])[0]) + "\n")
                    file.write("Its fitness (error) is: " + str(min(
                    self.fitness, key=lambda x: x[1])[1]) + "\n")

            # Evaluate each tree on the test set and store the best one
            for tree in self.population:
                error = self.evaluate_test_set(tree, test_set)
                if error < best_tree_error:
                    best_tree_error = error
                    best_tree = tree
        return best_tree