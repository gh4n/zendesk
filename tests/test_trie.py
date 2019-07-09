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
        self.words_in_trie = ["hi", "her", "he"]
        self.words_not_in_trie = ["nothere", "fire", "bad", "hopeless"]
        self.empty_string = ""

class TestCase:
    def __init__(self, string):
        self.string = string

class TestTrie(unittest.TestCase):

    data = TestData()

    def setUp(self):
        self.test_trie = Trie()
        self.test_case = TestCase(None)

    def _test_add(self, word, expected):
        self.test_trie.add(word)
        populated = self.test_trie.export()
        self.assertEqual(populated, expected)

    def _test_add_multiple_strings(self, words, expected):
        test_strings = list(map(TestCase, words))
        list(map(self.test_trie.add, test_strings))
        populated = self.test_trie.export()
        self.assertEqual(populated, expected)
    
    def _test_retrieve_word_true(self, test_case):
        self.test_trie.add(test_case)
        results = self.test_trie.retrieve(test_case.string)
        self.assertEqual(results[0], test_case)
    
    def test_add_string(self):
        self.test_case.string = self.data.string
        expected =b'{"t": {"e": {"s": {"t": {"i": {"n": {"g": {"\\u0000": {"storage": [{"string": "testing"}]}}}}}}}}}'.decode('utf-8')
        self._test_add(self.test_case, expected)

    def test_add_accented_string(self):
        self.test_case.string = self.data.accented_string
        expected = b'{"r": {"\\u00e9": {"s": {"u": {"m": {"\\u00e9": {"\\u0000": {"storage": [{"string": "r\\u00e9sum\\u00e9"}]}}}}}}}}'.decode('utf-8')
        self._test_add(self.test_case, expected)
    
    def test_add_integer_string(self):
        self.test_case.string = self.data.integer_string
        expected = b'{"1": {"2": {"3": {"t": {"e": {"s": {"t": {"i": {"n": {"g": {"1": {"2": {"3": {"\\u0000": {"storage": [{"string": "123testing123"}]}}}}}}}}}}}}}}}'.decode('utf-8')
        self._test_add(self.test_case, expected)
    
    def test_add_punctuated_string(self):
        self.test_case.string = self.data.punctuated_string
        expected = b'{".": {",": {"/": {"#": {"!": {"$": {"%": {"^": {"&": {"*": {";": {":": {"{": {"}": {"=": {"-": {"_": {"`": {"~": {")": {"(": {")": {"\\u0000": {"storage": [{"string": ".,/#!$%^&*;:{}=-_`~)()"}]}}}}}}}}}}}}}}}}}}}}}}}}'.decode('utf-8')
        self._test_add(self.test_case, expected)

    def test_space_delimited_string(self):
        self.test_case.string = self.data.space_delimited_string
        expected = b'{"t": {"h": {"i": {"s": {" ": {"i": {"s": {" ": {"m": {"e": {"\u0000": {"storage": [{"string": "this is me"}]}}}}}}}}}}}}'.decode('utf-8')
        self._test_add(self.test_case, expected)

    def test_add_empty_string(self):
        self.test_case.string = self.data.empty_string
        expected = b'{"\u0000": {"storage": [{"string": ""}]}}'.decode('utf-8')
        self._test_add(self.test_case, expected)

    def test_add_multiple_strings(self):
        strings = self.data.words_in_trie
        expected = b'{"h": {"i": {"\u0000": {"storage": [{"string": "hi"}]}}, "e": {"r": {"\u0000": {"storage": [{"string": "her"}]}}, "\u0000": {"storage": [{"string": "he"}]}}}}'.decode('utf-8')
        self._test_add_multiple_strings(strings, expected)

    def test_add_same_word_twice(self):
        words = ["once", "once"]
        expected = b'{"o": {"n": {"c": {"e": {"\u0000": {"storage": [{"string": "once"}, {"string": "once"}]}}}}}}'.decode('utf-8')
        self._test_add_multiple_strings(words, expected)

    def test_retrieve_string_true(self):
        self.test_case.string = self.data.string
        self._test_retrieve_word_true(self.test_case)
    
    def test_retrieve_accented_string_true(self):
        self.test_case.string = self.data.accented_string
        self._test_retrieve_word_true(self.test_case)
    
    def test_retrieve_integer_string_true(self):
        self.test_case.string = self.data.integer_string
        self._test_retrieve_word_true(self.test_case)
    
    def test_retrieve_punctuated_string_true(self):
        self.test_case.string = self.data.punctuated_string
        self._test_retrieve_word_true(self.test_case)
    
    def test_retrieve_space_delimited_string_true(self):
        self.test_case.string = self.data.space_delimited_string
        self._test_retrieve_word_true(self.test_case)
    
    def test_retrieve_words_false(self):
        words_not_in_trie = self.data.words_not_in_trie

        # create new TestCase object for each word
        words_in_trie = list(map(TestCase, self.data.words_in_trie))

        # insert test)cases into trie
        list(map(self.test_trie.add, words_in_trie))

        # query the trie with words_not_in_trie
        results = list(map(self.test_trie.retrieve, words_not_in_trie))
        for result in results:
            self.assertEqual(result, False)

    def test_retrieve_words_true(self):
        test_cases = list(map(TestCase, self.data.words_in_trie))
        list(map(self.test_trie.add, test_cases))

        results = list(map(lambda case: self.test_trie.retrieve(case.string), test_cases))
        for index, result in enumerate(results):
            self.assertEqual(result[0].string,  test_cases[index].string)

if __name__ == "__main__":
    unittest.main()
    

    