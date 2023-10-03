import collections
import random


class Tree():
    def __init__(self, root):
        self.root = root

    def crossover(self,):
        node1 = self.get_mutate_node(self.root)
        node2 = self.get_mutate_node(self.root)
        return

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

    def evaluate():
        return

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
