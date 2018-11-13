class Order:
    def __init__(self, oid):
        self.oid = oid
        self.park_id = None
        self.visitor_id = None
        self.amount = None
        self.type = None
        self.date = None
        self.payment_processing = {}

    def getAsJsonObject(self):
        return {"oid": str(self.oid),
                "pid": str(self.park_id),
                "date": self.date,
                "type": self.type,
                "amount": self.amount}

    def getVerboseJsonObject(self):
        return {
            "oid": str(self.oid),
            "pid": str(self.park_id),
            "amount": self.amount,
            "vid": str(self.visitor_id),
            "date": self.date,
            "payment_processing": self.payment_processing
        }
