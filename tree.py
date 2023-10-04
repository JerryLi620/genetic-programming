import collections
import random


class Tree():
    def __init__(self, root):
        self.root = root

    def crossover(self, other):
        node1 = self.select_random_node(self.root)
        node2 = self.select_random_node(other.root)

        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

    def mutate(self):
        node = self.get_random_leaf(self.root)
        # node.value = random.choice(node).value
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
            node.value = str(number)

    def evaluate(self, node, val):

        # missing base-case here
        
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
                raise ValueError("Division by zero")
            else:
                return left_val / right_val


    def get_random_node(self, node):
        stack = [node]
        nodes = []
        while stack:
            current = stack.pop()
            nodes.append(current)
            if current.left:
                stack.append(current.left)
            if current.right:
                stack.append(current.right)
        return random.choice(nodes)

    def get_random_leaf(self, node):
        queue = collections.deque([node])
        layers = []
        layer = collections.deque()
        while queue:
            cur = queue.popleft()
            if cur.left:
                layer.append(cur.left)
            if cur.right:
                layer.append(cur.right)
            if not queue and layer:
                queue = layer
                layers.append(layer)
                layer = collections.deque()
        return random.choice(layers[-1])


class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return self.data
