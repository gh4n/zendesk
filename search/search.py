# Solution assumes static JSON files, 
# ie. JSON file does not change while search is running
# split into 3 categories, users, tickets, orgs
import json
import yaml
from trie import Trie
from entry import Entry
from query import Query

class Search:
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
                    new_entry = Entry(index, str(item), field, group_name)
                    self.trie.add(new_entry)
            if type(entry[field]) is dict:
                self.add_entry(index, entry[field], field, group_name)
            else:
                new_entry = Entry(index, str(entry[field]), field, group_name)
                self.trie.add(new_entry)
                
    def freeform_search(self, user_query):
        query = Query(user_query)
        return self.trie.retrieve(query.string)
    
    def field_and_group_search(self, user_query, field, group):
        query = Query(user_query, field=field, group=group)
        unfiltered_results = self.freeform_search(query)
        filtered_results = self.filter_results(query, unfiltered_results)
        return filtered_results

    def filter_results(self, query, results):
        results = list(filter(lambda entry: entry.field == query.field, results))
        results = list(filter(lambda entry: entry.group == query.group, results))
        return results
    
    def _get_field(self, entry, field):
        raw_entry = self.get_raw(entry)
        return [self.get_attr(entry, field), self.get_attr(entry, "_id")]

    def get_name_ids(self, entries):
        return list(map(lambda entry: self._get_field(entry, "name"), entries))
    
    def get_subject_ids(self, entries):
        return list(map(lambda entry: self._get_field(entry, "subject"), entries))

    def get_raw(self, entry):
        data = self.groups[entry.group]
        return entry.get_raw(data)
    
    def get_attr(self, entry, field):
        data = self.groups[entry.group]
        return entry.get_attr(data, field)

    def get_related_info(self, entry):
        raw_entry = self.get_raw(entry)

        if entry.group == "orgs":
            related_results = self.field_and_group_search(raw_entry["_id"], field="organization_id", group="users")
            users = self.get_name_ids(related_results)
            entry.related_results["users"] = users

            related_results = self.field_and_group_search(raw_entry["_id"], field="organization_id", group="tickets")
            tickets = self.get_name_ids(related_results)
            entry.related_results["tickets"] = tickets

        if entry.group == "tickets":
            related_results = self.field_and_group_search(raw_entry["submitter_id"], field="_id", group="users")
            submitter = self.get_name_ids(related_results)
            entry.related_results["submitter"] = submitter

            related_results = self.field_and_group_search(raw_entry["assignee_id"], field="_id", group="users")
            assignee = self.get_name_ids(related_results)
            entry.related_results["assignee"] = assignee

            related_results = self.field_and_group_search(raw_entry["organization_id"], field="_id", group="orgs")
            org = self.get_name_ids(related_results)
            entry.related_results["org"] = org
        
        if entry.group == "users":
            related_results = self.field_and_group_search(raw_entry["organization_id"], field="_id", group="orgs")
            org = self.get_name_ids(related_results)
            entry.related_results["org"] = org

            related_results = self.field_and_group_search(raw_entry["_id"], field="assignee_id", group="tickets")
            assigned_tickets = self.get_subject_ids(related_results)
            entry.related_results["assigned_tickets"]=assigned_tickets

            related_results = self.field_and_group_search(raw_entry["_id"], field="submitter_id", group="tickets")
            submitted_tickets = self.get_subject_ids(related_results)
            entry.related_results["submitted_tickets"]=submitted_ticket

    def format_results(self, results):
        print("FORMAT", results)
        for entry in results:
            if entry.group == "users":
                print("hi")
                self.get_related_info(entry)
                self.format_user(entry)
            if entry.group == "orgs":
                self.format_org(entry)
            if entry.group == "tickets":
                self.format_ticket(entry)    
    
    def format_user(self, entry):
        order = ["name", "alias", "_id", "org","organization_id", "role", "email", "phone",
                    "locale", "timezone", "created_at", "active","verified", "shared", "url",
                    "external_id","tags", "suspended", "assigned_tickets", "submitted_tickets", "last_login_at"]
        raw_entry = entry.get_raw(self.users)
        for key in order:
            if key in ["org", "submitted_tickets", "assigned_tickets"]:
                print(entry.related_results[key])
            else:
                key_out = key[0].upper() + key[1:]
                print(f"{key_out}: {raw_entry[key]}")

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
                f = self.get_available_fields(self.users)
                fields_list = self.format_fields(f) 
                search_field = int(input("Which field would you like to search on? "))
                field = fields_list[search_field]
                user_query = input(f"{field} >>>> ")
                query = Query(user_query, group=group, field=field)
                results = self.freeforsearch(query)
                filtered = self.filter_results(query, results)
                self.format_results(filtered)

            if group == "orgs":
                f = self.get_available_fields(self.orgs)
                fields_list = self.format_fields(f) 
                search_field = int(input("Which field would you like to search on? "))
                field = fields_list[search_field]
                user_query = input(f"{field} >>>> ")
                query = Query(user_query)
                query.set_group("tickets")
                query.set_field(field)
                results = self.search(query)
                filtered = self.filter_results(query, results)


            if group == "tickets":
                f = self.get_available_fields(self.tickets)
                fields_list = self.format_fields(f) 
                search_field = int(input("Which field would you like to search on? "))
                field = fields_list[search_field]
                user_query = input(f"{field} >>>> ")
                query = Query(user_query)
                query.set_group("tickets")
                query.set_field(field)
                results = self.search(query)
                filtered = self.filter_results(query, results)
                print(filtered)
    
if __name__ == "__main__":
    search = Search(users_filepath="data/users.json", tickets_filepath="data/tickets.json", orgs_filepath="data/organizations.json")
    # q = "Pennsylvania"
    # res = search.search(q)
    # print(res.storage)
    
    # print(search.trie.export())
    # print(search.tickets[94])
