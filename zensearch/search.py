# Solution assumes static JSON files, 
# ie. JSON file does not change while search is running
# split into 3 categories, users, tickets, orgs

import json
import yaml
from trie import Trie

class Entry:
    def __init__(self, index, string, field, group):
        self.index = index
        self.string = string
        self.field = field
        self.group = group
        self.best_match = False

class SearchZendesk:
    """
    Reads in files
    Builds search tree
    """
    def __init__(self, users_filepath, tickets_filepath, orgs_filepath):
        self.users = self.load_file(users_filepath)
        self.tickets = self.load_file(tickets_filepath)
        self.orgs = self.load_file(orgs_filepath)
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
        for index, entry in enumerate(group):
            self.add_entry(index, entry, group_name)
    
    def add_entry(self, index, entry, group_name):
        for field in entry:
            if type(entry[field]) is list:
                for item in entry[field]:
                    item.lower()
                    new_entry = Entry([index], str(item), field, group_name)
                    self.trie.add(new_entry)
            if type(entry[field]) is dict:
                self.add_entry(index, entry[field], field, group_name)
            else:
                new_entry = Entry([index], str(entry[field]).lower(), field, group_name)
                self.trie.add(new_entry)
                
    def search(self, query):
        return self.trie.retrieve(query)
    
if __name__ == "__main__":
    search = SearchZendesk("data/users.json", "data/tickets.json", "data/organizations.json")
    # print(search.trie.export())
    print(search.tickets[94])
