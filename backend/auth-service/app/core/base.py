from abc import ABC, abstractmethod

class HashTableBase(ABC):
    @abstractmethod
    def put(self, key, value): pass
    
    @abstractmethod
    def get(self, key): pass
    
    @abstractmethod
    def remove(self, key): pass