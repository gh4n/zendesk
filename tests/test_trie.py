import context
from trie import Trie
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
        self.empty_string = ""


class TestString:
    def __init__(self, string):
        self.string = string


class TestTrie(unittest.TestCase):

    data = TestData()

    def setUp(self):
        self.test_trie = Trie()
        self.test_string = TestString(None)

    def _test_add(self, word, expected):
        self.test_trie.add(word)
        populated = self.test_trie.export()
        self.assertEqual(populated, expected)

    def _test_add_multiple_strings(self, words, expected):
        test_strings = list(map(TestString, words))
        list(map(self.test_trie.add, test_strings))
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
        self.test_string.string = self.data.string
        expected = b'{"t": {"e": {"s": {"t": {"i": {"n": {"g": {"\\u0000": {"storage": [{"string": "testing"}]}}}}}}}}}'
        self._test_add(self.test_string, expected)

    def test_add_accented_string(self):
        self.test_string.string = self.data.accented_string
        expected = b'{"r": {"\\u00e9": {"s": {"u": {"m": {"\\u00e9": {"\\u0000": {"storage": [{"string": "r\\u00e9sum\\u00e9"}]}}}}}}}}'
        self._test_add(self.test_string, expected)

    def test_add_integer_string(self):
        self.test_string.string = self.data.integer_string
        expected = b'{"1": {"2": {"3": {"t": {"e": {"s": {"t": {"i": {"n": {"g": {"1": {"2": {"3": {"\\u0000": {"storage": [{"string": "123testing123"}]}}}}}}}}}}}}}}}'
        self._test_add(self.test_string, expected)

    def test_add_punctuated_string(self):
        self.test_string.string = self.data.punctuated_string
        expected = b'{".": {",": {"/": {"#": {"!": {"$": {"%": {"^": {"&": {"*": {";": {":": {"{": {"}": {"=": {"-": {"_": {"`": {"~": {")": {"(": {")": {"\\u0000": {"storage": [{"string": ".,/#!$%^&*;:{}=-_`~)()"}]}}}}}}}}}}}}}}}}}}}}}}}}'
        self._test_add(self.test_string, expected)

    def test_space_delimited_string(self):
        self.test_string.string = self.data.space_delimited_string
        expected = b'{"t": {"h": {"i": {"s": {" ": {"i": {"s": {" ": {"m": {"e": {"\u0000": {"storage": [{"string": "this is me"}]}}}}}}}}}}}}'.encode(
            'utf-8')
        self._test_add(self.test_string, expected)

    def test_add_empty_string(self):
        self.test_string.string = self.data.space_delimited_string
        expected = b'{"\0": {"storage": [{"string": ""}]}}'.encode()
        self._test_add(self.test_string, expected)

    def test_add_multiple_strings(self):
        strings = self.data.words_in_trie
        expected = b'{"h": {"e": {"r": {"e": {"\\u0000": {"storage": [{"string": "here"}]}}}}, "i": {"r": {"e": {"\\u0000": {"storage": [{"string": "hire"}]}}}}, "o": {"p": {"e": {"\\u0000": {"storage": [{"string": "hope"}]}}}}}, "g": {"o": {"o": {"d": {"\\u0000": {"storage": [{"string": "good"}]}}}}}}'
        self._test_add_multiple_strings(strings, expected)

    def test_find_string_true(self):
        self.test_string.string = self.data.string
        self._test_find_word_true(self.test_string)

    def test_find_accented_string_true(self):
        self.test_string.string = self.data.accented_string
        self._test_find_word_true(self.test_string)

    def test_find_integer_string_true(self):
        self.test_string.string = self.data.integer_string
        self._test_find_word_true(self.test_string)

    def test_find_punctuated_string_true(self):
        self.test_string.string = self.data.punctuated_string
        self._test_find_word_true(self.test_string)

    def test_find_space_delimited_string_true(self):
        self.test_string.string = self.data.space_delimited_string
        self._test_find_word_true(self.test_string)

    def test_find_words_false(self):
        words_in_trie = self.data.words_in_trie
        words_not_in_trie = self.data.words_not_in_trie
        list(map(self.test_trie.add, words_in_trie))
        results = list(map(self.test_trie.find, words_not_in_trie))
        for result in results:
            self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
