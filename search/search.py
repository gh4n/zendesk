# Solution assumes static JSON files, 
# ie. JSON file does not change while search is running
# split into 3 categories, users, tickets, orgs

import json
import yaml
from trie import Trie

class Entry:
    """
    Generic object to reference the entry that is
    indexed into the Trie
    """
    def __init__(self, index, string, field, group):
        self.index = index
        self.string = string
        self.field = field
        self.group = group
        self.best_match = False

class Query:
    """
    Encapsulates the user's search choices
    """
    def __init__(self, query_string):
        self.string = query_string
        self.field = None
        self.group = None
    
    def set_field(self, field):
        self.field = field
    
    def set_group(self, group):
        self.group = group


class SearchZendesk:
    """
    Reads in files
    Builds search tree
    """
    def __init__(self, users_filepath=None, tickets_filepath=None, orgs_filepath=None):
        self.users = self.load_file(users_filepath)
        self.tickets = self.load_file(tickets_filepath)
        self.orgs = self.load_file(orgs_filepath)
        self.groups = {"users": self.users, "tickets": self.tickets, "orgs": self.orgs}
        self.trie = Trie()
        self.build_search()
        self.prompt()
    
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
                    new_entry = Entry([index], str(item), field, group_name)
                    self.trie.add(new_entry)
            if type(entry[field]) is dict:
                self.add_entry(index, entry[field], field, group_name)
            else:
                new_entry = Entry([index], str(entry[field]), field, group_name)
                self.trie.add(new_entry)
                
    def search(self, query):
        return self.trie.retrieve(query)

    def get_available_fields(self, group, fields={}):
        for item in group:
            for field in item:
                fields.setdefault(field, "X")
        return fields
    
    def get_all_available_fields(self):
        fields = {}
        for group in self.groups:
            fields = self.get_available_fields(group, fields)
        return fields
    
    def format_fields(self, fields):
        fields = list(fields.keys())
        for index, val in enumerate(fields):
            print(f"({index}) {val}")

        # TODO print("(A), All fields")
        return fields

    def prompt(self):
        print("Welcome to Zendesk Search!")
        query_type = input("What type of search would you like to make?\n[1] Freeform search\n[2] Field Search\n[3] Group Search\n")  
        if query_type == "1":
            user_query = input("Please enter query string >>>> ")
            query = Query(user_query)
        if query_type == "2":
            print(self.get_all_available_fields())
        if query_type =="3":
            group = input("Which group would you like to search on? (users, orgs, tickets) ")
            if group == "users":
                print(self.get_available_fields(self.users))
            if group == "orgs":
                print(self.get_available_fields(self.orgs))
            if group == "tickets":
                f = self.get_available_fields(self.tickets)
                fields_list = self.format_fields(f) 
                search_field = int(input("Which field would you like to search on? "))
                field = fields_list[search_field]
                user_query = input(f"{field} >>>> ")
                query = Query(user_query)
                query.set_group("tickets")
                query.set_field(field)
    
if __name__ == "__main__":
    search = SearchZendesk(users_filepath="data/users.json", tickets_filepath="data/tickets.json", orgs_filepath="data/organizations.json")
    # q = "Pennsylvania"
    # res = search.search(q)
    # print(res.storage)
    
    # print(search.trie.export())
    # print(search.tickets[94])
