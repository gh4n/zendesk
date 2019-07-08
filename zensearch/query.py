class Query:
    """
    Encapsulates the user's search choices
    """
    def __init__(self, user_query, field=None, group=None):
        self.string = self.process(user_query)
        self.field = field
        self.group = group
    
    def process(self, user_query):
        query_string = str(user_query).lower()
        return query_string


    