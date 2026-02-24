import math

class FibNode:
    def __init__(self, key, value):
        self.key = key          # The weight (e.g., distance/time)
        self.value = value      # The data (e.g., Driver ID)
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.marked = False     # Used for cascading cuts

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key, value):
        node = FibNode(key, value)
        if self.min_node is None:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min_node.key:
                self.min_node = node
        self.total_nodes += 1
        return node

    def _add_to_root_list(self, node):
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                # Add children to root list
                children = [x for x in self._get_nodes(z.child)]
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            
            # Remove z from root list
            z.left.right = z.right
            z.right.left = z.left

            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()
            self.total_nodes -= 1
        return z

    def _consolidate(self):
        # Golden ratio based size for the degree array
        max_degree = int(math.log2(self.total_nodes)) + 2
        A = [None] * max_degree
        
        root_nodes = [x for x in self._get_nodes(self.min_node)]
        for w in root_nodes:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        
        # Reconstruct root list and find new min
        self.min_node = None
        for node in A:
            if node is not None:
                if self.min_node is None:
                    self.min_node = node
                else:
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link(self, y, x):
        # Remove y from root list and make it a child of x
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if x.child is None:
            x.child = y
            y.right = y
            y.left = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.marked = False

    def _get_nodes(self, start_node):
        nodes = []
        curr = start_node
        if curr is None: return nodes
        while True:
            nodes.append(curr)
            curr = curr.right
            if curr == start_node: break
        return nodes