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