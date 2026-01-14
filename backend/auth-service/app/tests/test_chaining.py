import pytest
from app.core.chaining import HashTable

def test_put_and_get():
    table = HashTable()
    
    table.put("key", 1)
    table.put("key", 2)
    
    assert table.get("key") == 2
    
def test_remove_key():
    table = HashTable()
    
    table.put("key", "value")
    table.remove("key")
    
    assert table.get("key") is None
    
def test_hash_collision_handling():
    table = HashTable(capacity=1)
    
    table.put("a", 1)
    table.put("b",2)
    
    assert table.get("a") == 1
    assert table.get("b") == 2