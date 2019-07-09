import context
from search import Search
from entry import Entry
from query import Query
import unittest
import json


class TestData:
    def __init__(self):
        self.samples = "tests/test_data/samples.json"
        self.user = "tests/test_data/users_data.json"
        self.org = "tests/test_data/orgs_data.json"
        self.ticket = "tests/test_data/tickets_data.json"
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

    def test_add_entry(self):
        data  = self.test_data.load(self.test_data.samples)
        user = data["user"]
        search = Search(self.test_data.user, self.test_data.ticket, self.test_data.org)
        search.add_item(user, "users")

        # search trie on all fields of the document
        # verify that they can be retrieved
        for field, value in user.items():
            if type(value) is list:
                for index, item in enumerate(value):
                    entry = Entry(user, item, field, "users")
                    result = search.trie.retrieve(entry.string)[0]
                    expected = str(value[index]).lower()
                    self.assertEqual(expected, result.string)
            else:
                entry = Entry(user, user[field], field, "users")
                result = search.trie.retrieve(entry.string)[0]
                expected = str(value).lower()
                self.assertEqual(expected, result.string)

    def _test_freeform_search(self, test_search_term):
        search = Search(self.test_data.user, self.test_data.ticket, self.test_data.org)
        search.build_search()  
        query = Query(test_search_term, field="", group="")
        return search.freeform_search(query)
    
    def test_freeform_search_empty_string(self):
        # empty field "name" in users_data.json
        result = self._test_freeform_search("")                
        entry = result[0]
        self.assertEqual(entry.string, "")
        self.assertEqual(entry.field, "name")
        self.assertEqual(entry.group, "users")
    
    def test_freeform_search_multiple_results(self):
        results = self._test_freeform_search("104")
        for entry in results:
            if entry.group == "users":
                self.assertEqual(str(entry.data["_id"]), "3")
            if entry.group == "tickets":
                self.assertEqual(str(entry.data["_id"]), "4cce7415-ef12-42b6-b7b5-fb00e24f9cc1")

    def test_freeform_search_multiple_results(self):
        results = self._test_freeform_search("104")
        for entry in results:
            if entry.group == "users":
                self.assertEqual(str(entry.data["_id"]), "3")
            if entry.group == "tickets":
                self.assertEqual(str(entry.data["_id"]), "4cce7415-ef12-42b6-b7b5-fb00e24f9cc1")

if __name__ == "__main__":
    unittest.main()
