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
        self.multiline_string = """this
        is
        a
        multiline
        string"""

class TestTrie(unittest.TestCase):

    data = TestData()

    def _test_add(self, word, output):
        test_trie = Trie()
        test_trie.add(word)
        populated = str(test_trie.root)
        print(populated)
        self.assertEquals(populated, output)

    def _test_find_word_true(self, words):
        test_trie = Trie()
        list(map(test_trie.add, words))
        results = list(map(test_trie.find, words))
        for result in results:
            self.assertEquals(True, result)

    def test_add_string(self):
        string = self.data.string
        expected = "{'t': {'e': {'s': {'t': {'i': {'n': {'g': {'$': {}}}}}}}}}"
        self._test_add(string, expected)

    def test_add_accented_string(self):
        string = self.data.accented_string
        expected = "{'r': {'é': {'s': {'u': {'m': {'é': {'$': {}}}}}}}}"
        self._test_add(string, expected)
    
    def test_add_integer_string(self):
        string = self.data.integer_string
        expected = "{'1': {'2': {'3': {'t': {'e': {'s': {'t': {'i': {'n': {'g': {'1': {'2': {'3': {'$': {}}}}}}}}}}}}}}}"
        self._test_add(string, expected)
    
    def test_add_punctuated_string(self):
        string = self.data.punctuated_string
        expected = "{'.': {',': {'/': {'#': {'!': {'$': {'%': {'^': {'&': {'*': {';': {':': {'{': {'}': {'=': {'-': {'_': {'`': {'~': {')': {'(': {')': {'$': {}}}}}}}}}}}}}}}}}}}}}}}}"
        self._test_add(string, expected)

    def test_space_delimited_string(self):
        string = self.data.space_delimited_string
        expected = "{'t': {'h': {'i': {'s': {' ': {'i': {'s': {' ': {'m': {'e': {'$': {}}}}}}}}}}}}"
        self._test_add(string, expected)

    def test_multiline_string(self):
        string = self.data.multiline_string
        expected = "{'t': {'h': {'i': {'s': {'\n': {' ': {' ': {' ': {' ': {'i': {'s': {'\n': {' ': {' ': {' ': {' ': {'a': {'\n': {' ': {' ': {' ': {' ': {'m': {'u': {'l': {'t': {'i': {'l': {'i': {'n': {'e': {'\n': {' ': {' ': {' ': {' ': {'s': {'t': {'r': {'i': {'n': {'g': {'$': {}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}"
        self._test_add(string, expected)

if __name__ == "__main__":
    unittest.main()
    

    