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
    
    def _create_query(self, search_data_field, field, group):
        try:
            return Query(self.get_field(search_data_field), field=field, group=group)
        except KeyError:
            return None

    def get_related_queries(self):
        if self.group == "users":
            orgs = self._create_query("organization_id", "_id", "orgs")
            submitted_tickets = self._create_query("_id", "submitter", "tickets")
            assigned_tickets = self._create_query("_id", "assignee_id", "tickets")
            return {"orgs": orgs, "submitted_tickets": submitted_tickets, "assigned_tickets": assigned_tickets}

        if self.group == "orgs":
            users = self._create_query("_id", "organization_id", "users")
            tickets = self._create_query("_id", "organization_id", "tickets")
            return {"users": users, "tickets":tickets}

        if self.group == "tickets":
            submitter = self._create_query("submitter_id", "_id", "users")
            assignee = self._create_query("assignee_id", "_id", "users")
            org = self._create_query("organization_id", "_id", "orgs")
            return {"submitter": submitter, "assignee": assignee, "org": org}
              
    def save_related_results(self):
        for key, results in self.related_results.items():
            if not results:
                continue
            for index, entry in enumerate(results):
                if entry.group == "tickets":
                    id = entry.get_field("_id")
                    subject = entry.get_field("subject")
                    results[index] = f'{subject} | {id}'
                else:
                    id = entry.get_field("_id")
                    name = entry.get_field("name")
                    results[index] = f'{name} | {id}'
            self.data[key] = results
    
    def format(self):
        return yaml.dump(self.data, allow_unicode=True)


        




    

