
class Node:
    def __init__(self, item):
        self.item = item

# Create a trie to index each entry
# for O(N) search, where N = length of query
class Trie:
    def __init__(self):
        self.root = {}
        self.TERMINAL = "$"
    
    def add(self, word):
        if not word:
            raise ValueError("Empty string")
        
        current_node = self.root
        for char in word:
            current_node = current_node.setdefault(char, {})
        
        current_node.setdefault(self.TERMINAL, {})

    def find(self, word):
        if not word:
            raise ValueError("Empty string")

        current_node = self.root
        for char in word:
            if char in current_node:
                current_node = current_node[char]
            else:
                return False

        return self.TERMINAL in current_node
            
    def export(self):
        return self.root

if __name__ == "__main__":
    trie = Trie()
    trie.add("test")
    print(trie.find("test"))
    print(trie.export())