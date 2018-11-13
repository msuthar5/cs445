import os
import pickle
#from utils import *
from core.report import *

# initializing empty data storage
ser = {"id": 0}
obj = {"id": 0}


admission_report = Report(911)
revenue_report = Report(917)
admission_report.type = "admissions"
revenue_report.type = "revenue"
admission_report.name = "Admissions report"
revenue_report.name = "Revenue report"


obj["911"] = admission_report
obj["917"] = revenue_report

for file in os.listdir("data_storage"):
    f = open("data_storage/" + file, "wb+")
    if file == "report_data":
        f.write(pickle.dumps(obj))
    else:
        f.write(pickle.dumps(ser))
    f.close()
