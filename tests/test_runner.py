import test_trie
import context
import unittest

test_suite = unittest.TestLoader().loadTestsFromModule(test_trie)
res = unittest.TextTestRunner(verbosity=2).run(test_suite)