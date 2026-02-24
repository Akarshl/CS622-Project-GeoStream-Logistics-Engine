import pytest
from src.bloom_filter import BloomFilter
from src.radix_tree import RadixTree

def test_bloom_filter_logic():
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
    bf.add("malicious_user_88")
    
    # Test True Positive
    assert bf.check("malicious_user_88") is True
    # Test True Negative
    assert bf.check("clean_user_01") is False

def test_radix_tree_prefixes():
    rt = RadixTree()
    rt.insert("apple")
    rt.insert("apply")
    
    # Test exact match
    assert rt.search("apple") is True
    assert rt.search("apply") is True
    # Test partial prefix (should be false if not an end node)
    assert rt.search("app") is False 
    # Test non-existent
    assert rt.search("banana") is False

def test_radix_tree_split():
    rt = RadixTree()
    rt.insert("interact")
    rt.insert("interview")
    # Both share "inter", then split at 'a' and 'v'
    assert rt.search("interact") is True
    assert rt.search("interview") is True