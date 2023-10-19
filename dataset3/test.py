from gp import GeneticProgramming
from utils import *
import sympy as sp
from read_data import *
x = sp.symbols('x')


# Load dataset
dataset = read_csv("test.csv")

# Constants for the GeneticProgramming
POPULATION_SIZE = 20
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = [x, 1, 2, 3]
FUNCTION_SET = [sp.Add, sp.Mul, sp.sin, sp.log, sp.exp]
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
