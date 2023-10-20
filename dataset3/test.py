from gp import GeneticProgramming
from utils import *
# Load dataset
dataset = []

# Normalize the values to [-10,10]
with open("dataset3.csv", 'r') as file:
    lines = file.readlines()[1:]  # Skip the header
    for line in lines:
        x, fx = map(float, line.strip().split(','))
        dataset.append((x, fx))

# Constants for the GeneticProgramming
POPULATION_SIZE = 500
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = ["x", "1", "2"]
FUNCTION_SET = ["+", "-", "*", "/", "log", "sin", "e"]
EARLY_STOP_PROB = 0.1
CROSSOVER_RATE = 0.8
MIGRATION_RATE = 0.1
MIGRATION_SIZE = 20

# Initialize the GeneticProgramming
gp = GeneticProgramming(dataset, POPULATION_SIZE, MAX_DEPTH, MAX_GENERATIONS,
                        TERMINAL_SET, FUNCTION_SET, EARLY_STOP_PROB, CROSSOVER_RATE, MIGRATION_RATE, MIGRATION_SIZE)

# Run the genetic algorithm
NUM_RUN = 5
best_trees = gp.genetic_algorithm(NUM_RUN, CROSSOVER_RATE, MIGRATION_RATE)
# Evaluate the best individual in the final population
best_tree = min(gp.fitness, key=lambda x: x[1])[0]
print("The best tree is:", best_tree)
print("Its fitness (error) is:", min(gp.fitness, key=lambda x: x[1])[1])
