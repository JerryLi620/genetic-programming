from utils import generate_random_trees_list, train_test_split
import random


"""
Class for performing genetic programming.
"""


class GeneticProgramming:
    def __init__(self, dataset, population_size, max_depth, max_generations, terminal_set, function_set, early_stop, crossover_rate=0.7):
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
        self.population = generate_random_trees_list(
            population_size, max_depth, terminal_set, function_set, early_stop)
        self.fitness = self.generate_fitness()

    def generate_fitness(self):
        """
        Calculate and return the fitness for all trees in the population.
        """
        fitness = []
        for tree in self.population:
            fitness.append((tree, self.evaluate(tree)))
        return fitness

    def select_fit_nodes(self, tournament_ratio=20):
        """
        Randomly selects some individuals and returns the best among them through the Tournament selection method.

        Params:
        @tournament_ratio: Number of individuals to select for tournament.

        Return:
        The fittest individual from the tournament.
        """
        selected_for_tournament = random.sample(
            self.fitness, self.population_size//tournament_ratio)
        return max(selected_for_tournament, key=lambda x: x[1])[0]

    def reproduce(self, parents):
        """
        Create offspring from given parents.

        Params:
        @parents: List of trees to reproduce.

        Return: 
        List of offspring.
        """
        new_population = []
        for i in range(0, self.population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = parent1.crossover(parent2)
            new_population.extend([child1, child2])
        for child in new_population:
            if random.random() < (1 - self.crossover_rate):
                child.mutate()
        return new_population

    def evaluate(self, tree, regularization_lambda=0.01):
        """
        Evaluate the tree's performance on the TRAINING set with a penalty for tree depth to prevent overfitting.

        Params:
        @tree: The tree to evaluate.
        @regularization_lambda: Weight for depth penalty.

        Return: 
        The error with depth penalty.
        """
        error = 0
        for x, y in self.dataset:
            prediction = tree.evaluate_tree(tree.root, x)
            error += (prediction - y) ** 2
        depth_penalty = regularization_lambda * tree.get_depth()
        error += depth_penalty
        return error / len(self.dataset)

    def evaluate_test_set(self, tree, test_set):
        """
        Evaluate the tree's performance on the test set (no penalties).

        Params:
        @tree: The tree to evaluate.
        @test_set: Test dataset.

        Return: 
        Error on the test set.
        """
        error = 0
        for x, y in test_set:
            prediction = tree.evaluate_tree(tree.root, x)
            error += (prediction - y) ** 2
        return error / len(test_set)

    def terminate(self, satisfactory_fitness=0.1):
        """
        Check if the best fitness is below a threshold.

        Params:
        @satisfactory_fitness: Fitness threshold.

        Return: 
        True if best fitness is below the threshold, otherwise False.
        """
        best_fitness = min(self.fitness, key=lambda x: x[1])[1]
        if best_fitness <= satisfactory_fitness:
            return True

    def genetic_algorithm(self, num_run, crossover_rate, regularization_lambda=0.01):
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
            for _ in range(self.max_generations):
                new_population = []
                for i in range(self.population_size):
                    rand = random.random()

                    # Crossover
                    if rand < crossover_rate:
                        parent1 = self.select_fit_nodes()
                        parent2 = self.select_fit_nodes()
                        offspring1, offspring2 = parent1.crossover(parent2)
                        new_population.append(offspring1)
                        new_population.append(offspring2)

                    # Mutation
                    else:
                        individual = self.select_fit_nodes()
                        mutant = individual.mutate()
                        new_population.append(mutant)
                # Replace the old population with the new population
                self.population = new_population[:]
                self.generate_fitness()
                # Check termination criterion for the run (assuming it's a function)
                if self.terminate():
                    break

            # Evaluate each tree on the test set and store the best one
            for tree in self.population:
                error = self.evaluate_test_set(tree, test_set)
                if error < best_tree_error:
                    best_tree_error = error
                    best_tree = tree
        return best_tree
