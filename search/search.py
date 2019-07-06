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
        self.related_results = {}
    
    def get_raw(self, group_data):
        return group_data[self.index]

    def get_attr(self, group_data, attribute):
        return self.get_raw(group_data)[attribute]

class Query:
    """
    Encapsulates the user's search choices
    """
    def __init__(self, query_string, field=None, group=None):
        self.string = str(query_string)
        self.field = field
        self.group = group
    
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
    
    
    def get_related_info(self, entry):
        if entry.group == "orgs":
            raw_entry = self.orgs[entry.index] 
            query_org_users = Query(raw_entry["_id"], field="organization_id", group="users")
            query_org_users_results = self.search(query_org_users)
            org_users = self.filter_results(query_org_users, query_org_users_results)
            org_users_info = list(map(lambda user : [user.get_attr(self.users, "name"), user.get_attr(self.users, "_id")], org_users))
            entry.related_results = {"org_users": org_users_info}

            query_org_tickets = Query(raw_entry["_id"], field="organization_id", group="tickets")
            query_org_tickets_results = self.search(query_org_tickets)
            org_tickets = self.filter_results(query_org_tickets, query_org_tickets_results)
            org_tickets_info = list(map(lambda ticket : [ticket.get_attr(self.tickets, "subject"), user.get_attr(self.tickets, "_id")], org_tickets))
            entry.related_results = {"org_tickets": org_tickets_info}


        if entry.group == "tickets":
            raw_entry = self.tickets[entry.index] 

            query_ticket_submitter = Query(raw_entry["submitter_id"], field="_id", group="users")
            query_ticket_submitter_results = self.search(query_ticket_submitter)
            ticket_submitter = self.filter_results(query_ticket_submitter, query_ticket_submitter_results)
            submitter_info = list(map(lambda user : [user.get_attr(self.users, "name"), user.get_attr(self.users, "_id")], ticket_submitter))
            entry.related_results["submitter"]=submitter_info

            query_ticket_assignee = Query(raw_entry["assignee_id"], field="_id", group="users")
            query_ticket_assignee_results = self.search(query_ticket_assignee)
            ticket_assignee = self.filter_results(query_ticket_assignee, query_ticket_assignee_results)
            assignee_info = list(map(lambda user : [user.get_attr(self.users, "name"), user.get_attr(self.users, "_id")], ticket_assignee))
            entry.related_results["assignee"]=assignee_info

            query_ticket_org = Query(raw_entry["organization_id"], field="_id", group="orgs")
            query_ticket_org_results = self.search(query_ticket_org)
            ticket_org = self.filter_results(query_ticket_org, query_ticket_org_results)
            org_info = list(map(lambda org : [org.get_attr(self.orgs, "name"), org.get_attr(self.orgs, "_id")], ticket_org))
            entry.related_results["org"]=org_info
        
        if entry.group == "users":
            print(entry.index)
            raw_entry = self.users[entry.index]

            query_user_org = Query(raw_entry["organization_id"], field="_id", group="orgs")
            query_user_org_results = self.search(query_user_org)
            user_org = self.filter_results(query_user_org, query_user_org_results)
            print(user_org)
            user_org_info = list(map(lambda org : [org.get_attr(self.orgs, "name"), org.get_attr(self.orgs, "_id")], user_org))
            print(user_org_info)
            entry.related_results["org"] = user_org_info
            print(entry.related_results)

            query_assigned_tickets = Query(raw_entry["_id"], field="assignee_id", group="tickets")
            query_assigned_tickets_results = self.search(query_assigned_tickets)
            assigned_tickets = self.filter_results(query_assigned_tickets, query_assigned_tickets_results)
            assigned_ticket_info = list(map(lambda ticket : [ticket.get_attr(self.tickets, "subject"), ticket.get_attr(self.tickets, "_id")], assigned_tickets))
            entry.related_results["assigned_tickets"]=assigned_ticket_info


            query_submitted_tickets = Query(raw_entry["_id"], field="submitter_id", group="tickets")
            query_submitted_tickets_results = self.search(query_submitted_tickets)
            submitted_tickets = self.filter_results(query_submitted_tickets, query_submitted_tickets_results)
            submitted_ticket_info = list(map(lambda ticket : [ticket.get_attr(self.tickets, "subject"), ticket.get_attr(self.tickets,"_id")], submitted_tickets))
            entry.related_results["submitted_tickets"]=submitted_ticket_info
            print(entry.related_results)

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
                results = self.search(query)
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
    search = SearchZendesk(users_filepath="data/users.json", tickets_filepath="data/tickets.json", orgs_filepath="data/organizations.json")
    # q = "Pennsylvania"
    # res = search.search(q)
    # print(res.storage)
    
    # print(search.trie.export())
    # print(search.tickets[94])
