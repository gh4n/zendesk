import context
from zensearch.trie import Trie 
import unittest

class TestData:
    def __init__(self):
        self.string = "testing"
        self.accented_string = "résumé"
        self.integer_string = "123testing123"
        self.punctuated_string = ".,/#!$%^&*;:{}=-_`~)()"
        self.space_delimited_string = "this is me"
        self.multiline_string = "this\nis\na\nmultiline\nstring"

class TestTrie(unittest.main):

    def test_add_word(self, word, output):
        test_trie = Trie()
        populated = test_trie.add(string)
        self.assertEquals(populated, output)

    def test_find_string(self, words, query_string):
        test_trie = Trie()
        list(map(test_trie.add, words))


if __name__ == "__main__":
    unittest.main()
    

    