class Site:

    def __init__(self, json):
        self.id = json.get('id')
        self.label = json.get('label')