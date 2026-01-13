class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        
class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word:str):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    def delete(self, word: str):
        def _delete(node, word, depth):
            if not node:
                return False
            
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[depth]
            should_delete = _delete(node.children.get(char),word, depth + 1)
            
            if should_delete:
                del node.children[chr]
                return not node.is_end and len(node.children) == 0
            return False
        _delete(self.root, word.lower(), 0)
        
    def _dfs(self, node, prefix, results):
        if node.is_end:
            results.append(prefix)
            
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)
    
    def autocomplete(self, prefix:str):
        node = self.root
        prefix = prefix.lower()
        
        for char in prefix:
            if char not in node.children:
                return[]
            node = node.children[char]
            
        results = []
        self._dfs(node, prefix, results)
        return results