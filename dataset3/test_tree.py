from utils import *
from tree import *

terminal_set = ["x", "1", "2"]
function_set = ["+", "-", "*", "/", "log", "sin", "e"]
number_of_trees = 5
depth = 5
early_stop_prob = 0
trees = generate_random_trees_list(
    number_of_trees, depth, terminal_set, function_set, early_stop_prob)

t1 = trees[0]
t2 = trees[1]
new1, new2 = t1.crossover(t2)


dataset = []
with open("test.csv", 'r') as file:
    lines = file.readlines()[1:]  # Skip the header
    for line in lines:
        x, fx = line.strip().split(',')
        dataset.append((float(x), float(fx)))
total_absolute_error = 0
for x, y in dataset:
    prediction = t1.evaluate_tree(t1.root, x)
    absolute_error = abs(prediction - y)**2
    total_absolute_error += absolute_error
print(total_absolute_error/len(dataset))