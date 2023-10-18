from gp import GeneticProgramming
from utils import *
import math
# Load dataset
dataset = []
dataset = []

# Find min and max values
min_x = float('inf')
max_x = float('-inf')
min_fx = float('inf')
max_fx = float('-inf')

with open("dataset3/dataset3.csv", 'r') as file:
    lines = file.readlines()[1:]  # Skip the header
    for line in lines:
        x, fx = map(float, line.strip().split(','))
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_fx = min(min_fx, fx)
        max_fx = max(max_fx, fx)

# Normalize the values to [-10,10]
with open("dataset3/dataset3.csv", 'r') as file:
    lines = file.readlines()[1:]  # Skip the header
    for line in lines:
        x, fx = map(float, line.strip().split(','))
        normalized_x = ((x - min_x) / (max_x - min_x)) * 20 - 10
        normalized_fx = ((fx - min_fx) / (max_fx - min_fx)) * 20 - 10
        dataset.append((normalized_x, normalized_fx))

# Constants for the GeneticProgramming
POPULATION_SIZE = 200
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = ["x"] + [str(i) for i in range(-1, 2)]
FUNCTION_SET = ["+", "-", "*", "/", "sin", "log", "e"]
EARLY_STOP_PROB = 0.1
CROSSOVER_RATE = 0.9

# Initialize the GeneticProgramming
gp = GeneticProgramming(dataset, POPULATION_SIZE, MAX_DEPTH, MAX_GENERATIONS,
                        TERMINAL_SET, FUNCTION_SET, EARLY_STOP_PROB, CROSSOVER_RATE)

# Run the genetic algorithm
NUM_RUN = 5
best_trees = gp.genetic_algorithm(NUM_RUN, CROSSOVER_RATE)
# Evaluate the best individual in the final population
best_tree = min(gp.fitness, key=lambda x: x[1])[0]
print("The best tree is:", best_tree)
print("Its fitness (error) is:", min(gp.fitness, key=lambda x: x[1])[1])
