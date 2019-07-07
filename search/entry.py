from query import Query
import yaml
    
class Entry:
    """
    Generic object to reference the entry that is
    indexed into the Trie
    """
    def __init__(self, data, string, field, group):
        self.string = string
        self.field = field
        self.group = group
        self.data = data
        self.related_results = {}

    def get_field(self, field):
        return self.data[field]

    def get_related_queries(self):
        if self.group == "users":
            orgs = Query(self.get_field("organization_id"), field = "_id", group="orgs")
            submitted_tickets = Query(self.get_field("_id"), field = "submitter", group="tickets")
            assigned_tickets = Query(self.get_field("_id"), field="assignee_id", group="tickets")
            return {"orgs": orgs, "submitted_tickets": submitted_tickets, "assigned_tickets": assigned_tickets}

        if self.group == "orgs":
            users = Query(self.get_field("_id"), field="organization_id", group="users")
            tickets = Query(self.get_field("_id"), field="organization_id", group="tickets")
            return {"users": users, "tickets":tickets}

        if self.group == "tickets":
            submitter = Query(self.get_field("submitter_id"), field="_id", group="users")
            assignee = Query(self.get_field("assignee_id"), field="_id",group="users")
            org = Query(self.get_field("organization_id"), field="_id", group="orgs")
            return {"submitter": submitter, "assignee": assignee, "org": org}
              
    def save_related_results(self):
        for key, results in self.related_results.items():
            for entry in results:
                if entry.group == "tickets":
                    id = entry.get_field("_id")
                    subject = entry.get_field("subject")
                    entry = f'{subject} | {id}'
                else:
                    id = entry.get_field("_id")
                    name = entry.get_field("name")
                    entry = f'{name} | {id}'
            self.data[key] = results
    
    def format(self):
        return yaml.dump(self.data)


        




    

