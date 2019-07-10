from trie import Trie
from entry import Entry
from query import Query
import json
import sys


class Search:
    """
    Search builds a search trie out of specified data.
    This class encompasses the functionality to do with 
    searching on User, Ticket, and Orgs data specifically.
    Groups: "users", "tickets", "orgs"
    """
    def __init__(self, users_filepath, tickets_filepath, orgs_filepath):
        self.users = self.load_file(users_filepath)
        self.tickets = self.load_file(tickets_filepath)
        self.orgs = self.load_file(orgs_filepath)
        self.groups = {"users": self.users, "tickets": self.tickets, "orgs": self.orgs}
        self.user_fields = self.get_fields(self.users)
        self.org_fields = self.get_fields(self.orgs)
        self.ticket_fields = self.get_fields(self.tickets)
        self.trie = Trie()
    
    def load_file(self, filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError as err:
            print(f"File: {filepath}, not found!")
            raise (err)
        except ValueError as err:
            print(f"File: {filepath}, could not be loaded!")
            raise (err)

    def build_search(self):
        self.add_group(self.users, "users")
        self.add_group(self.tickets, "tickets")
        self.add_group(self.orgs, "orgs")

    def add_group(self, group, group_name):
        for item in group:
            self.add_item(item, group_name)

    def add_item(self, item_data, group_name):
        # creates Entry for all the field values in each user, ticket and org
        # this is then inserted into the trie
        for field, value in item_data.items():
            if type(value) is list:
                for search_term in value:
                    new_entry = Entry(item_data, search_term, field, group_name)
                    self.trie.add(new_entry)
            else:
                new_entry = Entry(item_data, value, field, group_name)
                self.trie.add(new_entry)

    # search across all groups
    def freeform_search(self, query):
        return self.trie.retrieve(query.string)
    
    # filters a freeform search by group and field
    def field_and_group_search(self, query=None, query_string=None, field=None, group=None):
        if not query:
            query = Query(query_string, field, group)
        unfiltered_results = self.freeform_search(query)
        if not unfiltered_results:
            return None
        else:
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
        print(f'{result.group[0].upper()}{result.group[1:-1]}')
        print(result.format())

    def output_results(self, results):
        if not results:
            print("No Results Found!")
            return 
            
        print(f"{len(results)} found!")
        for result in results:
            self.output_result(result)
    
    def get_fields(self, group_data):
        fields = {}
        for entry in group_data:
            for field, value in entry.items():
                fields.setdefault(field, None)
        return fields
    
    def format_fields(self, fields):
        for field in fields:
            print(field)
    
    def prompt_group(self, group, group_fields):
        print("The following fields are available for searching on")
        self.format_fields(group_fields)
        chosen_field = input("Please enter the name of the field you wish to search on\n >>>> ")
        if chosen_field in group_fields:
            user_query = input("Please enter a search query\n >>>> ")
            results = self.field_and_group_search(query_string=user_query, field=chosen_field, group=group)
            self.output_results(results)
        else:
            print("Please enter a correct field")
        
    def prompt(self):
        choice = None
        while choice != "quit":
            print("\n\nHi Welcome to Zendesk Search. Please enter one of the following options\nFreeform, Users, Organizations, Tickets")
            choice = input(" >>>> ").lower()
            if choice == "freeform":
                user_query = input("Please enter a search query: \n >>>> ")
                query = Query(user_query)
                results = self.freeform_search(query)
                self.output_results(results)
            if choice == "users":
                self.prompt_group("users", self.user_fields)
            if choice == "tickets":
                self.prompt_group("tickets", self.ticket_fields)
            if choice == "organizations":
                self.prompt_group("orgs", self.org_fields)
            if choice == "quit":
                sys.exit()
            
if __name__ == "__main__":
    s = Search(
        users_filepath="data/users.json",
        tickets_filepath="data/tickets.json",
        orgs_filepath="data/organizations.json",
    )
    s.build_search()
    s.prompt()