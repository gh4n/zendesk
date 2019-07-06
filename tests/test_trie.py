import context
from search.trie import Trie 
import unittest
import json

class TestData:
    def __init__(self):
        self.string = "testing"
        self.accented_string = "résumé"
        self.integer_string = "123testing123"
        self.punctuated_string = ".,/#!$%^&*;:{}=-_`~)()"
        self.space_delimited_string = "this is me"
        self.words_in_trie = ["here", "hire", "good", "hope"]
        self.words_not_in_trie = ["nothere", "fire", "bad", "hopeless"]

class TestTrie(unittest.TestCase):

    data = TestData()

    def setUp(self):
        self.test_trie = Trie()

    def _test_add(self, word, expected):
        self.test_trie.add(word)
        populated = self.test_trie.export()
        self.assertEqual(populated, expected)

    def _test_add_multiple_strings(self, words, expected):
        list(map(self.test_trie.add, words))
        populated = self.test_trie.export()
        self.assertEqual(populated, expected)
    
    def _test_find_word_true(self, word):
        self.test_trie.add(word)
        result = self.test_trie.find(word)
        self.assertEqual(result, True)
    
    def _test_find_words_true(self, words):
        list(map(self.test_trie.add, words))
        results = list(map(self.test_trie.find, words))
        for result in results:
            self.assertEqual(result, True)
    
    def test_add_string(self):
        string = self.data.string
        expected = '{"t": {"e": {"s": {"t": {"i": {"n": {"g": {"$": {}}}}}}}}}'
        self._test_add(string, expected)

    def test_add_accented_string(self):
        string = self.data.accented_string
        expected = '{"r": {"é": {"s": {"u": {"m": {"é": {"$": {}}}}}}}}'
        self._test_add(string, expected)
    
    def test_add_integer_string(self):
        string = self.data.integer_string
        expected = '{"1": {"2": {"3": {"t": {"e": {"s": {"t": {"i": {"n": {"g": {"1": {"2": {"3": {"$": {}}}}}}}}}}}}}}}'
        self._test_add(string, expected)
    
    def test_add_punctuated_string(self):
        string = self.data.punctuated_string
        expected = '{".": {",": {"/": {"#": {"!": {"$": {"%": {"^": {"&": {"*": {";": {":": {"{": {"}": {"=": {"-": {"_": {"`": {"~": {")": {"(": {")": {"$": {}}}}}}}}}}}}}}}}}}}}}}}}'
        self._test_add(string, expected)

    def test_space_delimited_string(self):
        string = self.data.space_delimited_string
        expected = '{"t": {"h": {"i": {"s": {" ": {"i": {"s": {" ": {"m": {"e": {"$": {}}}}}}}}}}}}'
        self._test_add(string, expected)

    def test_add_multiple_strings(self):
        strings = self.data.words_in_trie
        expected = '{"h": {"e": {"r": {"e": {"$": {}}}}, "i": {"r": {"e": {"$": {}}}}, "o": {"p": {"e": {"$": {}}}}}, "g": {"o": {"o": {"d": {"$": {}}}}}}'
        self._test_add_multiple_strings(strings, expected)

    def test_find_string_true(self):
        string = self.data.string
        self._test_find_word_true(string)
    
    def test_find_accented_string_true(self):
        string = self.data.accented_string
        self._test_find_word_true(string)
    
    def test_find_integer_string_true(self):
        string = self.data.integer_string
        self._test_find_word_true(string)
    
    def test_find_punctuated_string_true(self):
        string = self.data.punctuated_string
        self._test_find_word_true(string)
    
    def test_find_space_delimited_string_true(self):
        string = self.data.space_delimited_string
        self._test_find_word_true(string)
    
    def test_find_words_false(self):
        words_in_trie = self.data.words_in_trie
        words_not_in_trie = self.data.words_not_in_trie
        list(map(self.test_trie.add, words_in_trie))
        results = list(map(self.test_trie.find, words_not_in_trie))
        for result in results:
            self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()
    

    