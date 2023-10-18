from gp import GeneticProgramming
from utils import *

# print("Test 1: Initialization and Population Generation")
# terminal_set = ['x'] + [str(i) for i in range(-5, 6)]
# function_set = ['+', '-', '*', '/']
# gp = GeneticProgramming(
#     dataset=[(i, i * 2) for i in range(10)],
#     population_size=100,
#     max_depth=3,
#     max_generations=3,
#     terminal_set=terminal_set,
#     function_set=function_set,
#     early_stop=0.1
# )
# print("Initial population:")
# for tree, fitness in gp.fitness:
#     # Print the root of each tree for simplicity. You might want to add a method to print the whole tree.
#     print(tree)

# # Test 2: Selection of Fit Nodes
# print("\nTest 2: Selection of Fit Nodes")
# selected_tree = gp.select_fit_nodes()
# print("Selected tree for tournament:", selected_tree)

# # Test 3: Reproduction and Crossover
# print("\nTest 3: Reproduction and Crossover")
# parents = [gp.select_fit_nodes() for _ in range(gp.population_size)]
# new_population = gp.reproduce(parents)
# print("New population after reproduction:")
# for tree in new_population:
#     print(tree)

# # Test 4: Termination Criteria
# print("\nTest 4: Termination Criteria")
# # You may need to adjust the values based on your actual results
# result = gp.terminate()
# print("Should terminate?", result)

# # Test 5: Main Genetic Algorithm Execution
# print("\nTest 5: Main Genetic Algorithm Execution")
# final_population = gp.genetic_algorithm(num_run=10, crossover_prob=0.7)
# for tree in new_population:
#     print(tree)
# print("Final population after genetic algorithm:")
# print(gp.eval_best_child())
# print("Best Child:", max(gp.fitness, key=lambda x: x[1])[0])


# Load dataset
dataset = []
with open("dataset1.csv", 'r') as file:
    lines = file.readlines()[1:]  # Skip the header
    for line in lines:
        x, fx = line.strip().split(',')
        dataset.append((float(x), float(fx)))

# Constants for the GeneticProgramming
POPULATION_SIZE = 200
MAX_DEPTH = 3
MAX_GENERATIONS = 200
TERMINAL_SET = ["x"] + [str(i) for i in range(-1, 2)]
FUNCTION_SET = ["+", "-", "*", "/"]
EARLY_STOP_PROB = 0.1
CROSSOVER_RATE = 0.5

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
