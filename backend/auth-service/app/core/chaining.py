from .base import HashTableBase

class HashTable(HashTableBase):
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.table = [[] for _ in range(self.capacity)]
        
    def _hash(self, key):   
        return hash(key) % self.capacity
    
    def put(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        
    def get(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def remove(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        self.table[index] = [(k, v) for k, v in bucket if k != key]