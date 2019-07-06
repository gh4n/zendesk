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
