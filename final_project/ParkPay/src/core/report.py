class Report:
    def __init__(self, rid, name=None,start_date=None, end_date=None, total_orders=None):
        self.rid = rid
        self.start_date = ""
        self.end_date = ""
        self.name = ""
        self.type = None
        self.total_admissions = 0
        self.total_orders = 0
        self.total_revenue = 0
        self.detail_by_park = []


    def getAsJsonObject(self):

        obj = {"rid": str(self.rid),
               "name": self.name,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "detail_by_park": self.detail_by_park
                }
        if self.type == "admissions":
            obj["total_admissions"] = self.total_admissions
        else:
            obj["total_orders"] = self.total_orders
            obj["total_revenue"] = self.total_revenue

        return obj

    def getSimpleJsonObject(self):
        return {"rid": str(self.rid), "name": self.name}

