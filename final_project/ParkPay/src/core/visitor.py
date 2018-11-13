class Visitor:
    def __init__(self, vid):
        self.vid = vid
        self.name = None
        self.email = None
        self.vehicle = None
        self.payment_info = None

    def getAsJsonObject(self):
        return_obj = {}
        return_obj["name"] = self.name
        return_obj["email"] = self.email
        return_obj["payment_info"] = self.payment_info
        return_obj["payment_info"]["card"] = "x" * 11 + self.payment_info["card"][-4:]
        return return_obj

    def getSimpleJsonObject(self):
        return {"vid": str(self.vid),
                "name": self.name,
                "email": self.email}