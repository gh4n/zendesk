import context
from search import Search
from entry import Entry
import unittest
import json


class TestData:
    def __init__(self):
        self.user = "tests/test_data/user_sample.json"
        self.org = "tests/test_data/org_sample.json"
        self.ticket = "tests/test_data/ticket.json"
        self.malformed_json = "tests/test_data/bad_input.json"

    def load(self, filepath):
        with open(filepath, "r") as f:
            return json.load(f)


class TestSearch(unittest.TestCase):
    test_data = TestData()

    def test_malformed_input_file(self):
        malformed = "tests/test_data/bad_input.json"
        acceptable = self.test_data.org
        even_better = self.test_data.user
        self.assertRaises(ValueError, lambda: Search(malformed, acceptable, even_better))

    def test_file_not_found(self):
        exists = self.test_data.user
        exists_as_well = self.test_data.org
        missing = "not_a_real_file.json"
        self.assertRaises(FileNotFoundError, lambda: Search(exists, exists_as_well, missing))

    def test_add_entry_user(self):
        user = self.test_data.load(self.test_data.user)
        ticket = self.test_data.load(self.test_data.ticket)
        org = self.test_data.load(self.test_data.org)

        search = Search(user, ticket, org)
        search.add_item(user, "users")

        for field, value in user.items():
            if type(value) is list:
                for index, item in enumerate(value):
                    entry = Entry(user, item, field, "users")
                    result = search.trie.retrieve(entry)[0]
                    self.assertEqual(field[index], result.string)
            else:
                entry = Entry(item, user[field], field, "users")
    
    def test_freeform_search():
        pass

    def test_filter_results():
        pass
    
    def test_output_results():
        pass
    
    def test_field_and_group_search():
        pass

if __name__ == "__main__":
    unittest.main()
