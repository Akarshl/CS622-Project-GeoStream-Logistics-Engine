import math
import hashlib

class BloomFilter:
    """
    A probabilistic data structure for set membership testing.
    Standard list-based 'bit array' implementation for educational clarity.
    """
    def __init__(self, expected_elements: int, false_positive_rate: float):
        # Parameters for the filter size and hash count
        self.n = expected_elements
        self.p = false_positive_rate
        
        # Calculate optimal bit array size (m) and hash functions (k)
        # Formula: m = -(n * ln(p)) / (ln(2)^2)
        self.m = int(-(self.n * math.log(self.p)) / (math.log(2) ** 2))
        
        # Formula: k = (m/n) * ln(2)
        self.k = int((self.m / self.n) * math.log(2))
        
        # Initialize bit array as a list of Booleans
        self.bit_array = [False] * self.m

    def _get_hashes(self, item: str):
        """Generates k different indices for an item using seeded hashing."""
        indices = []
        for i in range(self.k):
            # Use SHA-256 and append a seed 'i' to get different hash values
            hash_input = f"{item}{i}".encode('utf-8')
            digest = hashlib.sha256(hash_input).hexdigest()
            # Map hash to bit array index
            index = int(digest, 16) % self.m
            indices.append(index)
        return indices

    def add(self, item: str):
        """Adds an item to the filter by setting bits at k indices to True."""
        for index in self._get_hashes(item):
            self.bit_array[index] = True

    def check(self, item: str) -> bool:
        """
        Checks if an item is likely in the set.
        Returns False: Definitely not in the set.
        Returns True: Probably in the set (might be a false positive).
        """
        for index in self._get_hashes(item):
            if not self.bit_array[index]:
                return False
        return True

    def get_stats(self):
        """Returns metadata for the discrete math report."""
        return {
            "size_bits": self.m,
            "hash_functions": self.k,
            "false_positive_rate": self.p
        }