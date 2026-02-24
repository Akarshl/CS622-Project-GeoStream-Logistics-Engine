class BoundingBox:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x, self.min_y = min_x, min_y
        self.max_x, self.max_y = max_x, max_y

    def area(self):
        return max(0, self.max_x - self.min_x) * max(0, self.max_y - self.min_y)

    def contains(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    @staticmethod
    def from_points(points):
        if not points: return None
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return BoundingBox(min(xs), min(ys), max(xs), max(ys))

    @staticmethod
    def merge(box1, box2):
        """Returns a new MBR that contains both input boxes."""
        if not box1: return box2
        if not box2: return box1
        return BoundingBox(
            min(box1.min_x, box2.min_x),
            min(box1.min_y, box2.min_y),
            max(box1.max_x, box2.max_x),
            max(box1.max_y, box2.max_y)
        )

class RTreeNode:
    def __init__(self, is_leaf=True, max_entries=4):
        self.is_leaf = is_leaf
        self.max_entries = max_entries
        self.entries = []  # Leaf: [(x, y), data], Internal: [MBR, child_node]
        self.mbr = None

class RTree:
    def __init__(self, max_entries=4):
        self.root = RTreeNode(is_leaf=True, max_entries=max_entries)
        self.max_entries = max_entries

    def insert(self, point, data):
        node = self._choose_leaf(self.root, point)
        node.entries.append((point, data))
        if len(node.entries) > self.max_entries:
            self._split(node)
        # Fix: Now we actually update the MBRs up the tree
        self._update_mbrs(self.root)

    def _update_mbrs(self, node):
        """Recursively updates the Bounding Box for a node based on its children."""
        if not node.entries:
            return None
        
        if node.is_leaf:
            # For leaves, MBR is based on the (x, y) points
            points = [entry[0] for entry in node.entries]
            node.mbr = BoundingBox.from_points(points)
        else:
            # For internal nodes, MBR is the union of children's MBRs
            new_mbr = None
            for _, child in node.entries:
                child_mbr = self._update_mbrs(child)
                new_mbr = BoundingBox.merge(new_mbr, child_mbr)
            node.mbr = new_mbr
        return node.mbr

    def _choose_leaf(self, node, point):
        if node.is_leaf:
            return node
        # For this demo, we dive into the first child
        # A full implementation would pick the one needing least area expansion
        return self._choose_leaf(node.entries[0][1], point)

    def _split(self, node):
        mid = len(node.entries) // 2
        new_node = RTreeNode(is_leaf=node.is_leaf, max_entries=self.max_entries)
        new_node.entries = node.entries[mid:]
        node.entries = node.entries[:mid]
        return new_node

    def search(self, x, y, radius):
        results = []
        query_box = BoundingBox(x - radius, y - radius, x + radius, y + radius)
        self._search_recursive(self.root, query_box, results)
        return results

    def _search_recursive(self, node, query_box, results):
        if not node.mbr: return # Empty node
        
        for entry, data in node.entries:
            if node.is_leaf:
                if query_box.contains(entry[0], entry[1]):
                    results.append((entry, data))
            else:
                # 'data' is the child_node in internal nodes
                child_node = data
                if self._boxes_intersect(query_box, child_node.mbr):
                    self._search_recursive(child_node, query_box, results)

    def _boxes_intersect(self, b1, b2):
        if not b1 or not b2: return False
        return not (b1.max_x < b2.min_x or b1.min_x > b2.max_x or
                    b1.max_y < b2.min_y or b1.min_y > b2.max_y)