from gp import GeneticProgramming
from utils import *
from read_data import load_dataset

dataset = load_dataset("dataset2.csv")

# Constants for the GeneticProgramming
POPULATION_SIZE = 200
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = ["x1", "x2", "x3", "1", "-1"]
FUNCTION_SET = ["+", "-", "*", "/"]
EARLY_STOP_PROB = 0.3
CROSSOVER_RATE = 0.7

# Initialize the GeneticProgramming
gp = GeneticProgramming(dataset, POPULATION_SIZE, MAX_DEPTH, MAX_GENERATIONS,
                        TERMINAL_SET, FUNCTION_SET, EARLY_STOP_PROB, CROSSOVER_RATE)

# Run the genetic algorithm
NUM_RUN = 5
best_trees = gp.genetic_algorithm(NUM_RUN, CROSSOVER_RATE)
# Evaluate the best individual in the final population
best_tree = min(gp.fitness, key=lambda x: x[1])[0]

with open("results.txt", 'a') as file:
    file.write("The final best tree is: " + str(best_tree) + "\n")
    file.write("Its final fitness (error) is: " + str(min(gp.fitness, key=lambda x: x[1])[1]) + "\n")