from trie import Trie
from entry import Entry
from query import Query
import json


class Search:
    def __init__(self, users_filepath=None, tickets_filepath=None, orgs_filepath=None):
        self.users = self.load_file(users_filepath)
        self.tickets = self.load_file(tickets_filepath)
        self.orgs = self.load_file(orgs_filepath)
        self.groups = {"users": self.users, "tickets": self.tickets, "orgs": self.orgs}
        self.trie = Trie()
        self.build_search()

    def load_file(self, filepath):
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                return json.load(f)
        except FileNotFoundError as err:
            print(f"File: {filepath}, not found!", err)
        except ValueError as err:
            print(f"File: {filepath}, could not be loaded!", err)

    def build_search(self):
        self.add_group(self.users, "users")
        self.add_group(self.tickets, "tickets")
        self.add_group(self.orgs, "orgs")

    def add_group(self, group, group_name):
        for entry in group:
            self.add_entry(entry, group_name)

    def add_entry(self, entry, group_name):
        for field in entry:
            if type(entry[field]) is list:
                for item in entry[field]:
                    new_entry = Entry(entry, item, field, group_name)
                    self.trie.add(new_entry)
            else:
                new_entry = Entry(entry, entry[field], field, group_name)
                self.trie.add(new_entry)

    def freeform_search(self, query):
        return self.trie.retrieve(query.string)

    def field_and_group_search(self, query=None, query_string=None, field=None, group=None):
        if not query:
            query = Query(query_string, field, group)
        unfiltered_results = self.freeform_search(query)
        return self.filter_results(query, unfiltered_results)

    def filter_results(self, query, results):
        if query.field:
            results = list(filter(lambda entry: entry.field == query.field, results))
        if query.group:
            results = list(filter(lambda entry: entry.group == query.group, results))
        return results

    def output_result(self, result):
        queries = result.get_related_queries()
        for key, query in queries.items():
            result.related_results[key] = self.field_and_group_search(query)
        result.save_related_results()
        print(result.format())

    def output_results(self, results):
        if not results:
            print("No search results!")
            return
        for result in results:
            self.output_result(result)

if __name__ == "__main__":
    s = Search(
        users_filepath="data/users.json",
        tickets_filepath="data/tickets.json",
        orgs_filepath="data/organizations.json",
    )
    # res = s.field_and_group_search(query_string="Fédératéd Statés Of Micronésia", field="", group="" )
    res = s.field_and_group_search(query_string="", field="", group="")
    s.output_results(res)
