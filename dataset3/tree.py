import random
import copy
import sympy as sp
import random


x = sp.symbols('x')


class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)


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
        choices = ["constant", "variable", "unary_function"]
        choice = random.choice(choices)
        if choice == "constant":
            node.value = random.randint(-3, 3)
        elif choice == "variable":
            node.value = x
        else:
            node.value = random.choice(
                [sp.sin, sp.log, sp.exp])  # Use SymPy functions
            # Ensure the node has only a left child
            node.right = None
            if not node.left:
                node.left = Node(x)
        return new_tree

    def evaluate_tree(self, node, val):
        if not node.left and not node.right:
            if isinstance(node.value, sp.Symbol):
                result = node.value.subs(x, val)
                if result == sp.zoo:
                    return float('inf')
                return result.evalf()
            else:
                return node.value

        left_val = self.evaluate_tree(node.left, val) if node.left else None
        right_val = self.evaluate_tree(node.right, val) if node.right else None

        # For unary functions
        if node.value in [sp.sin, sp.log, sp.exp]:

            return node.value(left_val).evalf()

        # For binary operators
        return node.value(left_val, right_val).evalf()

    def get_random_node(self):
        return random.choice(self.nodes)

    def get_random_leaf(self):
        return random.choice(self.leaf)

    def __str__(self):
        expr = self.tree_to_sympy_expr(self.root)
        return str(expr)

    def tree_to_sympy_expr(self, node):
        if not node.left and not node.right:
            return node.value

        if node.value in [sp.sin, sp.log, sp.exp]:  # Unary functions
            return node.value(self.tree_to_sympy_expr(node.left))

        # For binary operations
        return node.value(self.tree_to_sympy_expr(node.left), self.tree_to_sympy_expr(node.right))
