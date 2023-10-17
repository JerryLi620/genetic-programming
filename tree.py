from collections import deque
import random

class Tree():
    def __init__(self, root):
        self.root = root

        stack = [self.root]
        self.leaf = []
        self.nodes = []
        while stack:
            cur = stack.pop()
            self.nodes.append(cur)
            if cur.left:
                stack.append(cur.left)
            if cur.right:
                stack.append(cur.right)
            if not cur.left and not cur.right:
                self.leaf.append(cur)

    def crossover(self, other):
        tree1 = Tree(self.root)
        tree2 = Tree(other.root)

        node1 = tree1.get_random_node()
        node2 = tree2.get_random_node()

        # Swap the values
        node1.value, node2.value = node2.value, node1.value

        # Swap the children
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right
        
        return tree1, tree2


    def mutate(self):
        new_tree = Tree(self.root)
        node = new_tree.get_random_leaf()
        choices = ["constant", "variable"]
        if node.value.isnumeric():
            choice = random.choice(choices)
            if choice == "constant":
                options = [1, -1]
                option = random.choice(options)
                node.value = int(node.value)+option
            else:
                node.value = "x"
        else:
            number = random.randint(-3, 3)
            print(number)
            node.value = str(number)

    def evaluate(self, node, val):
        if not node.left and not node.right:
            if node.value == 'x':
                return val
            else:
                return int(node.value)

        left_val = self.evaluate(node.left, val)
        right_val = self.evaluate(node.right, val)

        if node.value == '+':
            return left_val + right_val
        if node.value == '-':
            return left_val - right_val
        if node.value == '*':
            return left_val * right_val
        if node.value == '/':
            if right_val == 0:
                return 0
            else:
                return left_val / right_val

    def get_random_node(self):
        return random.choice(self.nodes)

    def get_random_leaf(self):
        return random.choice(self.leaf)
    
class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return self.data


# # Test cases here
# # Test 1: Complex Tree Creation and Evaluation
# node1 = Node("x")
# node2 = Node("5")
# node3 = Node("+", node1, node2)

# node4 = Node("x")
# node5 = Node("3")
# node6 = Node("-", node4, node5)

# node7 = Node("*", node3, node6)

# node8 = Node("2")
# root1 = Node("/", node7, node8)

# tree1 = Tree(root1)

# print("Initial complex tree1 evaluation for x=4:", tree1.evaluate(tree1.root, 4))

# # Test 2: Mutation
# tree1.mutate()
# print("Complex tree1 after mutation, evaluation for x=4:", tree1.evaluate(tree1.root, 4))

# # Test 3: Crossover
# node9 = Node("x")
# node10 = Node("2")
# node11 = Node("*", node9, node10)

# node12 = Node("x")
# node13 = Node("3")
# node14 = Node("/", node12, node13)

# root2 = Node("-", node11, node14)

# tree2 = Tree(root2)

# print("Initial complex tree2 evaluation for x=4:", tree2.evaluate(tree2.root, 4))

# tree1.crossover(tree2)

# print("Complex tree1 after crossover, evaluation for x=4:", tree1.evaluate(tree1.root, 4))
# print("Complex tree2 after crossover, evaluation for x=4:", tree2.evaluate(tree2.root, 4))