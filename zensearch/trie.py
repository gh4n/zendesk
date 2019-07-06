
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

        if self.TERMINAL in current_node:
            print("True")
            return current_node[self.TERMINAL]
        else:
            return False
            
    def export(self):
        return self.root

if __name__ == "__main__":
    trie = Trie()
    trie.add("Hello this is \nme")
    trie.find("Hello this is \nme")
    # print(trie.export())

    words = ["hey", "im", "grace"]
    trie.add("hey")
    list(map(trie.add, words))
    trie.find("grace")
    trie.find("im")
    print(trie.export())
