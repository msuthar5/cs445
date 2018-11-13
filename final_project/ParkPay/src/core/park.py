class Park:
    def __init__(self, pid):
        self.pid = pid
        self.note_ids = []
        self.name = None
        self.region = None
        self.address = None
        self.phone = None
        self.web = None
        self.geo = None
        self.payment_info = {}

    def toJsonObject(self, detail):
        obj = {}
        obj["pid"] = str(self.pid)
        linfo = {}
        linfo["name"] = self.name
        linfo["region"] = self.region
        linfo["address"] = self.address
        linfo["phone"] = self.phone
        linfo["web"] = self.web
        linfo["geo"] = self.geo

        if detail == True:
            obj["payment_info"] = self.payment_info

        obj["location_info"] = linfo
        return obj