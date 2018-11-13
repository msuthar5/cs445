class Note:
    def __init__(self, nid, date):
        self.nid = nid
        self.date = date
        self.name = None
        self.park_id = None
        self.text = None
        self.title = None
        self.visitor_id = None

    def getAsJsonObject(self):
        return {
                "nid": str(self.nid),
                "date": self.date,
                "title": self.title
            }

