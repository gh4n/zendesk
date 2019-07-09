import jsons
from entry import Entry


class TerminalNode:
    """
    TerminalNodes exist as the leaf nodes of the trie, 
    that is - at the end of words key'd by the TERMINAL.
    These allow objects to be stored at the end of search terms.
    """

    def __init__(self):
        self.storage = []

    def add(self, item):
        self.storage.append(item)


class Trie:
    """
    Dictionary based trie to index each search words.
    """

    def __init__(self):
        self.root = {}
        self.TERMINAL = "\0"

    def add(self, entry):
        if not entry.string:
            self.set_terminal_node(self.root, entry)
            return

        current_node = self.root
        for char in entry.string:
            current_node = current_node.setdefault(char, {})

        if self.TERMINAL in current_node:
            terminal_node = current_node[self.TERMINAL]
            terminal_node.add(entry)
        else:
            self.set_terminal_node(current_node, entry)

    def set_terminal_node(self, current_node, item):
        terminal_node = TerminalNode()
        terminal_node.add(item)
        current_node[self.TERMINAL] = terminal_node

    def retrieve(self, string):
        if not string and self.TERMINAL in self.root:
            return self.root[self.TERMINAL].storage

        current_node = self.root
        for char in string:
            if char in current_node:
                current_node = current_node[char]
            else:
                return False

        if self.TERMINAL not in current_node:
            return False

        return current_node[self.TERMINAL].storage

    def export(self):
        return jsons.dumps(self.root)


if __name__ == "__main__":

    class TestString:
        def __init__(self, string):
            self.string = string

    trie = Trie()

    t = TestString("hi")

    trie.add(t)

    print(trie.export())
