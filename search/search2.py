from trie import Trie
from entry import Entry
from query import Query
import json
class ZendeskSearch():
    def __init__(self, users_filepath=None, tickets_filepath=None, orgs_filepath=None):
        self.users = self.load_file(users_filepath)
        self.tickets = self.load_file(tickets_filepath)
        self.orgs = self.load_file(orgs_filepath)
        self.groups = {"users": self.users, "tickets": self.tickets, "orgs": self.orgs}
        self.trie = Trie()
        self.build_search()
    
    def load_file(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
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
                    new_entry = Entry(entry, str(item), field, group_name)
                    self.trie.add(new_entry)
            if type(entry[field]) is dict:
                self.add_entry(entry, entry[field], field, group_name)
            else:
                new_entry = Entry(entry, str(entry[field]), field, group_name)
                self.trie.add(new_entry)

    def freeform_search(self, query):
        return self.trie.retrieve(query.string)
    
    def field_and_group_search(self, query=None, query_string=None, field=None, group=None):
        if not query:
            query = Query(query_string, field, group)
        unfiltered_results = self.freeform_search(query)
        return self.filter_results(query, unfiltered_results)

    def filter_results(self, query, results):
        filtered_fields = list(filter(lambda entry: entry.field == query.field, results))
        return list(filter(lambda entry: entry.group == query.group, filtered_fields))
    
    def output_result(self, result):
        queries = result.get_related_queries()
        print(queries)
        for key, query in queries.items():
            result.related_results[key]  = self.field_and_group_search(query)
        result.save_related_results()
        result.format()

    def output_results(self, results):
        for result in results:
            self.output_result(result)
        
if __name__ == "__main__":
    s = ZendeskSearch(users_filepath="data/users.json", tickets_filepath="data/tickets.json", orgs_filepath="data/organizations.json")
    # s.build_search()
    # class Query:
    #     def __init__(self):
    #         self.string = "http://initech.zendesk.com/api/v2/organizations/113.json"
    # query = Query()
    res = s.field_and_group_search(query_string="Massachusetts", field="tags", group="tickets" )
    s.output_results(res)

    # print(s.trie.export())