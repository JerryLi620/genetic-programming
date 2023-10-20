from utils import *
import random
import math


class GeneticProgramming:
    def __init__(self, dataset, population_size, max_depth, max_generations, terminal_set, function_set, early_stop, crossover_rate, migration_rate, migration_size):
        """
        Initialize the genetic programming class

        Params:
        @dataset: Data to evolve trees.
        @population_size: Size of the population.
        @max_depth: Maximum depth of the trees.
        @max_generations: Number of generations for the algorithm.
        @terminal_set: Set of terminals (leaf nodes) for the tree.
        @function_set: Set of function nodes for the trees.
        @early_stop: Stopping criterion.
        @crossover_rate: Probability of crossover during reproduction.
        """
        self.dataset = dataset
        self.population_size = population_size
        self.max_depth = max_depth
        self.max_generations = max_generations
        self.terminal_set = terminal_set
        self.function_set = function_set
        self.early_stop = early_stop
        self.migration_rate = migration_rate
        self.migration_size = migration_size
        # self.population = generate_random_trees_list(
        #     population_size, max_depth, terminal_set, function_set, early_stop)
        # self.fitness = self.generate_fitness()
        self.crossover_rate = crossover_rate

    def generate_fitness(self, train_set):
        """
        Calculate and return the fitness for all trees in the population.
        """
        fitness = []
        for tree in self.population:
            fitness.append((tree, self.evaluate(train_set, tree)))
        return fitness

    def select_fit_nodes(self, tournament_ratio=100):
        """
        Randomly selects some individuals and returns the best among them through the Tournament selection method.

        Params:
        @tournament_ratio: Number of individuals to select for tournament.

        Return:
        The fittest individual from the tournament.
        """
        selected_for_tournament = random.sample(
            self.fitness, self.population_size//tournament_ratio)
        return min(selected_for_tournament, key=lambda x: x[1])[0]

    def evaluate(self, train_set, tree, regularization_lambda=1000):
        """
        Evaluate the tree's performance on the TRAINING set with a penalty for tree depth to prevent overfitting.

        Params:
        @tree: The tree to evaluate.
        @regularization_lambda: Weight for depth penalty.

        Return: 
        The error with depth penalty.
        """

        total_error = 0
        for x, y in train_set:
            prediction = tree.evaluate_tree(tree.root, x)
            try:
                error = abs(prediction - y)**2
            except:
                error = float("inf")
            total_error += error
            depth_penalty = regularization_lambda * tree.get_depth()
            total_error += depth_penalty
        return total_error/len(train_set)

    def evaluate_test_set(self, tree, test_set):
        """
        Evaluate the tree's performance on the test set (no penalties).

        Params:
        @tree: The tree to evaluate.
        @test_set: Test dataset.

        Return: 
        Error on the test set.
        """
        total_error = 0
        for x, y in test_set:
            prediction = tree.evaluate_tree(tree.root, x)
            try:
                error = abs(prediction - y)**2
            except:
                error = float("inf")
            total_error += error
        return total_error/len(test_set)

    def terminate(self, satisfactory_fitness=0.1):
        """
        Check if the best fitness is below a threshold.

        Params:
        @satisfactory_fitness: Fitness threshold.

        Return: 
        True if best fitness is below the threshold, otherwise False.
        """
        best_fitness = min(self.fitness, key=lambda x: x[1])[1]
        return best_fitness <= satisfactory_fitness

    def genetic_algorithm(self, num_run, crossover_rate, migration_rate):
        """
        Main genetic algorithm loop for evolving trees.

        Params:
        @num_run: Number of runs for the genetic algorithm.
        @crossover_rate: Probability for crossover.
        @regularization_lambda: Weight for depth penalty.

        Return: 
        Best tree from all runs.
        """

        # Split the dataset into train and test sets
        train_set, test_set = train_test_split(self.dataset)
        self.dataset = train_set  # Set the dataset to the training set for evaluation

        best_tree = None
        best_tree_error = float('inf')

        for _ in range(num_run):
            print("start")
            self.population = generate_random_trees_list(
                self.population_size, self.max_depth, self.terminal_set, self.function_set, self.early_stop)
            print("population created")
            self.fitness = self.generate_fitness(train_set)
            print("fitness created")
            for i in range(self.max_generations):
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
                self.fitness = self.generate_fitness(train_set)
                # Check termination criterion for the run
                if self.terminate():
                    print("terminate")
                    print("The best tree is:", min(
                        self.fitness, key=lambda x: x[1])[0])
                    print("Its fitness (error) is:", min(
                        self.fitness, key=lambda x: x[1])[1])
                    break
                print("The best tree is:", min(
                    self.fitness, key=lambda x: x[1])[0])
                print("Its fitness (error) is:", min(
                    self.fitness, key=lambda x: x[1])[1])

            # Evaluate each tree on the test set and store the best one
            for tree in self.population:
                error = self.evaluate_test_set(tree, test_set)
                if error < best_tree_error:
                    best_tree_error = error
                    best_tree = tree
        return best_tree
