from utils import *
from tree import *

x = sp.symbols('x')
terminal_set = [x, 1, 2, 3]
function_set = [sp.Add, sp.Mul, sp.sin, sp.log, sp.exp]
number_of_trees = 5
depth = 5
early_stop_prob = 0
trees = generate_random_trees_list(
    number_of_trees, depth, terminal_set, function_set, early_stop_prob)

t1 = trees[0]
t2 = trees[1]
new1, new2 = t1.crossover(t2)
print(new1.evaluate_tree(new1.root, 3))
