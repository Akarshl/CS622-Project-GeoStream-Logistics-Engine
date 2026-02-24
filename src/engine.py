from .bloom_filter import BloomFilter
from .radix_tree import RadixTree
from .r_tree import RTree
from .fibonacci_heap import FibonacciHeap

class LogisticsEngine:
    def __init__(self):
        # 1. Security: Block known malicious IDs
        self.security_filter = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # 2. Search: Store valid city locations/merchants
        self.location_search = RadixTree()
        
        # 3. Spatial: Store active driver coordinates
        self.driver_index = RTree(max_entries=4)
        
        # 4. Storage for distance/routing results
        self.routing_priority = FibonacciHeap()

    def add_driver(self, driver_id, coords):
        self.driver_index.insert(coords, driver_id)

    def add_location(self, name):
        self.location_search.insert(name)

    def blacklist_user(self, user_id):
        self.security_filter.add(user_id)

    def find_best_driver(self, user_id, destination_name, user_coords):
        # Step 1: Bloom Filter Check
        if self.security_filter.check(user_id):
            return "ACCESS DENIED: User ID flagged by security filter."

        # Step 2: Radix Tree Check
        if not self.location_search.search(destination_name):
            return f"ERROR: Location '{destination_name}' not found in registry."

        # Step 3: R-Tree Spatial Search (Radius of 10 units)
        nearby_drivers = self.driver_index.search(user_coords[0], user_coords[1], 10)
        
        if not nearby_drivers:
            return "No drivers found in your area."

        # Step 4: Fibonacci Heap for Ranking
        # We calculate Euclidean distance and use it as the 'key'
        for coords, d_id in nearby_drivers:
            dist = ((coords[0]-user_coords[0])**2 + (coords[1]-user_coords[1])**2)**0.5
            self.routing_priority.insert(dist, d_id)

        # Extract the minimum (closest) driver
        best_match = self.routing_priority.extract_min()
        return f"Success! Driver {best_match.value} assigned. Distance: {best_match.key:.2f} units."