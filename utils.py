import random
from tree import *


def generate_random_trees_list(number, depth, terminal_set, function_set, early_stop_prob):
    trees = []
    for _ in range(number):
        node = generate_random_nodes(
            None, depth, terminal_set, function_set, early_stop_prob, is_root=True)
        trees.append(Tree(node))
    return trees


def generate_random_nodes(node, depth, terminal_set, function_set, early_stop_prob, is_root=False):
    if depth == 0 or random.random() < early_stop_prob:
        # Only select from terminal_set if depth is 0 or with early stopping probability
        node = Node(random.choice(terminal_set))
    else:
        # Select from function_set otherwise
        node = Node(random.choice(function_set))

    if node.value in function_set and depth > 0:  # if the node is a function/operator and not at max depth
        node.left = generate_random_nodes(
            node.left, depth-1, terminal_set, function_set, early_stop_prob)
        node.right = generate_random_nodes(
            node.right, depth-1, terminal_set, function_set, early_stop_prob)

    return node


def train_test_split(dataset, test_ratio=0.2):
    random.shuffle(dataset)
    test_size = int(len(dataset) * test_ratio)
    test_set = dataset[:test_size]
    train_set = dataset[test_size:]
    return train_set, test_set

# terminal_set = ['+', '-', '*', '/']
# function_set = ['x'] + [str(i) for i in range(-5, 6)]

# res = generate_random_nodes_set(5, 5, function_set, terminal_set, 0.1)
# print(res)
