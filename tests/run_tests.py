import test_trie
import test_entry
import test_search
import context
import unittest

trie_test_suite = unittest.TestLoader().loadTestsFromModule(test_trie)
unittest.TextTestRunner(verbosity=2).run(trie_test_suite)

entry_test_suite = unittest.TestLoader().loadTestsFromModule(test_entry)
unittest.TextTestRunner(verbosity=2).run(entry_test_suite)

search_test_suite = unittest.TestLoader().loadTestsFromModule(test_search)
unittest.TextTestRunner(verbosity=2).run(search_test_suite)

