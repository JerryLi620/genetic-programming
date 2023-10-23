from gp import GeneticProgramming
from utils import *
from read_data import load_dataset
import random


def create_subset(dataset, fraction=0.1):
    """
    Returns a subset of the data.
    """
    subset_size = int(len(dataset) * fraction)
    return random.sample(dataset, subset_size)


# Load dataset
dataset = load_dataset("new_dataset2.csv")

# Constants for the GeneticProgramming
POPULATION_SIZE = 500
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = ["x1", "x2", "x3", "1","2"]
FUNCTION_SET = ["+", "-", "*", "/"]
EARLY_STOP_PROB = 0.1
CROSSOVER_RATE = 0.7
MIGRATION_RATE = 0.2
MIGRATION_SIZE = 30

# Get a subset of the dataset
fraction = 0.1
subset = create_subset(dataset, fraction)

# Initialize the GeneticProgramming with the subset
gp = GeneticProgramming(subset, POPULATION_SIZE, MAX_DEPTH, MAX_GENERATIONS,
                        TERMINAL_SET, FUNCTION_SET, EARLY_STOP_PROB, CROSSOVER_RATE, MIGRATION_RATE, MIGRATION_SIZE)

# Run the genetic algorithm
NUM_RUN = 5
best_trees = gp.genetic_algorithm(NUM_RUN, CROSSOVER_RATE, MIGRATION_RATE)

# Evaluate the best individual in the final population
best_tree = min(gp.fitness, key=lambda x: x[1])[0]
error_full_data = gp.evaluate_test_set(best_tree, dataset)

# Log results
with open("results.txt", 'a') as file:
    file.write("The final best tree is: " + str(best_tree) + "\n")
    file.write("Its final fitness (error) on the subset is: " + str(min(gp.fitness, key=lambda x: x[1])[1]) + "\n")
    file.write("Error of best tree on the full dataset: " + str(error_full_data) + "\n")
