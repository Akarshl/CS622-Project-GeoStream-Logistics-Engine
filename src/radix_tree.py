class RadixNode:
    def __init__(self, prefix="", is_end=False):
        self.prefix = prefix
        self.is_end = is_end
        self.children = {}  # Map of first character -> RadixNode

class RadixTree:
    def __init__(self):
        self.root = RadixNode()

    def _get_common_prefix_length(self, s1, s2):
        length = 0
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                break
            length += 1
        return length

    def insert(self, word):
        curr = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in curr.children:
                # Case 1: No matching edge, just create a new one
                curr.children[char] = RadixNode(word[i:], True)
                return
            
            child = curr.children[char]
            common = self._get_common_prefix_length(word[i:], child.prefix)
            
            if common < len(child.prefix):
                # Case 2: Partial match - SPLIT the node
                # New intermediate node representing the 'common' part
                split_node = RadixNode(child.prefix[:common], False)
                # Old child prefix is shortened to the 'suffix' part
                child.prefix = child.prefix[common:]
                
                # Re-assign children
                split_node.children[child.prefix[0]] = child
                curr.children[char] = split_node
                
                # Check if the new word ends at the split or needs a new branch
                if i + common == len(word):
                    split_node.is_end = True
                else:
                    new_suffix = word[i + common:]
                    split_node.children[new_suffix[0]] = RadixNode(new_suffix, True)
                return
            
            # Case 3: Full match of prefix, keep traversing
            i += common
            curr = child
        
        curr.is_end = True

    def search(self, word):
        curr = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in curr.children:
                return False
            child = curr.children[char]
            if not word[i:].startswith(child.prefix):
                return False
            i += len(child.prefix)
            curr = child
        return curr.is_end