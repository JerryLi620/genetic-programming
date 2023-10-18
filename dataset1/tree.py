import random
import copy


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

    def get_depth(self, node=None):
        if not node:
            node = self.root
        if not node.left and not node.right:
            return 1
        left_depth = self.get_depth(node.left) if node.left else 0
        right_depth = self.get_depth(node.right) if node.right else 0
        return 1 + max(left_depth, right_depth)

    def crossover(self, other):
        tree1 = Tree(copy.deepcopy(self.root))
        tree2 = Tree(copy.deepcopy(other.root))

        node1 = tree1.get_random_node()
        node2 = tree2.get_random_node()

        # Swap the values
        node1.value, node2.value = node2.value, node1.value

        # Swap the children
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

        return tree1, tree2

    def mutate(self):
        new_tree = Tree(copy.deepcopy(self.root))
        node = new_tree.get_random_leaf()
        choices = ["constant", "variable"]
        if node.value.isnumeric():
            choice = random.choice(choices)
            if choice == "constant":
                options = [1, -1]
                option = random.choice(options)
                node.value = str(int(node.value)+option)
            else:
                node.value = "x"
        else:
            number = random.randint(-3, 3)
            node.value = str(number)
        return new_tree

    def evaluate_tree(self, node, val):
        if not node.left and not node.right:
            if node.value == 'x':
                return val
            else:
                return int(node.value)

        left_val = self.evaluate_tree(node.left, val)
        right_val = self.evaluate_tree(node.right, val)

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

    def __str__(self):
        return self._inorder_string(self.root)

    def _inorder_string(self, node):
        if not node:
            return ""

        # If leaf node
        if not node.left and not node.right:
            return str(node.value)

        left_str = self._inorder_string(node.left)
        right_str = self._inorder_string(node.right)

        return f"({left_str} {node.value} {right_str})"


class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return self.value


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

# print("Initial complex tree1 evaluation for x=4:",
#       tree1.evaluate_tree(tree1.root, 4))

# # Test 2: Mutation
# tree1.mutate()
# print("Complex tree1 after mutation, evaluation for x=4:",
#       tree1.evaluate_tree(tree1.root, 4))

# # Test 3: Crossover
# node9 = Node("x")
# node10 = Node("2")
# node11 = Node("*", node9, node10)

# node12 = Node("x")
# node13 = Node("3")
# node14 = Node("/", node12, node13)

# root2 = Node("-", node11, node14)

# tree2 = Tree(root2)

# print("Initial complex tree2 evaluation for x=4:",
#       tree2.evaluate_tree(tree2.root, 4))

# tree1.crossover(tree2)

# print("Complex tree1 after crossover, evaluation for x=4:",
#       tree1.evaluate_tree(tree1.root, 4))
# print("Complex tree2 after crossover, evaluation for x=4:",
#       tree2.evaluate_tree(tree2.root, 4))
