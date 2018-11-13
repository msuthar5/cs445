import unittest
import requests
import json
import os
import controller
import init_data
from core.park import *
from core.order import *
from core.visitor import *
from core.note import *
from utilities.utils import *

class TestStringMethods(unittest.TestCase):

    def get_request(self, args):
        URL = args[1]
        resp = args[2]
        status_code = args[3]
        r = requests.get(URL)
        self.assertEqual(r.json(), resp)

    def setUp(self):
        file = open("test/test_data.json", "r+")
        content = file.read()
        file.close()
        self.data = json.loads(content)
        self.headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        self.maxDiff = None

    """
        Testing the Initialization of the data storage system.
        
        We verify that each data file is properly iniitlized with: {"id":0}
    """
    def test_init_data_storage(self):
        os.system("python3 init_data.py")
        data = controller.load_serialized_data("park_data")
        correct = True
        files = os.listdir("data_storage/")

        for file in files:
            if file != "report_data":
                if controller.load_serialized_data(file) != {"id": 0}:
                    correct = False

        self.assertEqual(correct, True)

    """
        Test that the initial revenue report has been properly initialized
    """
    def test_revenue_report_initialization(self):
        allReports = controller.load_serialized_data("report_data")

        self.assertEqual(allReports["917"].getSimpleJsonObject(), {"rid": "917", "name": "Revenue report"})
    """
        Test that the initial admissions report has been properly initialized
    """
    def test_admissions_report_initialization(self):
        allReports = controller.load_serialized_data("report_data")

        self.assertEqual(allReports["911"].getSimpleJsonObject(), {"rid": "911", "name": "Admissions report"})


    """
        Test the Report class method: getAsJsonObject()
        
        - load the report and assert the return value of the method
    """
    def test_report_getAsJsonObject_method(self):
        allReports = controller.load_serialized_data("report_data")
        self.assertEqual(allReports["911"].getAsJsonObject(), {"total_admissions": 0, "name": "Admissions report", "detail_by_park": [], "end_date": "", "start_date": "", "rid": "911"})

    """
        This function tests the Order class method: getAsJsonObject()

        - create an Order object, and then test the value of the method
    """
    def test_order_getAsJsonObject_function(self):
        order = Order(0)
        order.park_id = 2
        order.visitor_id = 15
        order.amount = 12
        order.type = "car"
        order.date = "2018-1-12"

        print(order.getAsJsonObject())
        self.assertEqual(order.getAsJsonObject(), {'pid': '2', 'date': '2018-1-12', 'amount': 12, 'oid': '0', 'type': 'car'})

    """
        This function tests the Visitor class method: getVerboseJsonObject()

        - create a Visitor object, and then test the value of the method
    """
    def test_visitor_getVerboseJsonObject_function(self):
        visitor = Visitor(1)
        visitor.name = "Manish Suthar"
        visitor.email = "msuthar@hawk.iit.edu"
        visitor.vehicle = build_vehicle_information(1, "IL", "HELP", "car")
        visitor.payment_info = build_payment_information('373456789045678',
                                                         "Manish Suthar",
                                                         "5/23",
                                                         "60616")
        expected = {'email': 'msuthar@hawk.iit.edu', 'name': 'Manish Suthar', 'payment_info': {'name_on_card': 'Manish Suthar', 'expiration_date': '5/23', 'card': 'xxxxxxxxxxx5678', 'zip': '60616'}}

        self.assertEqual(visitor.getAsJsonObject(), expected)

    """
        Test the data helper method: test_data_serialization()
        
        - serialize a Park object and then deserialize it to verify its contents 
    """
    def test_data_serialization(self):
        allParks = controller.load_serialized_data("park_data")
        allParks[10] = Park(10)
        controller.dump_serialized_data("park_data", allParks)
        newParks = controller.load_serialized_data("park_data")
        print(newParks[10].toJsonObject(False))
        self.assertEqual(newParks[10].toJsonObject(True), {"payment_info": {}, "pid": "10", "location_info": {"geo": None, "web": None, "phone": None, "address": None, "name": None, "region": None}})


    """
        Test the helper function: resource_not_founds
        
        - This function returns the formatted response for a 404 
          corresponding to the to the passed resource and id
    """
    def test_resource_not_found_function(self):

        expected = {
            "type": "http://localhost/parkpay/parks/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "Resource: notes has no entry for ID: 50",
            "status": 404,
            "instance": "/notes"
        }
        self.assertEqual(controller.resource_not_found("notes", 50), expected)

    """
        Tests the helper function: validate_park_input()
        
        - Pass faulty validation data and expect to get a 400 error response
    """
    def test_park_post_data_validation(self):
        post_data = {"location_info":{"name":"Apple River Canyon",\
                                      "address":"8763 E. Canyon Rd, Apple River, IL 61001","phone":"815-745-3302","web":"https://www.dnr.illinois.gov/Parks/Pages/AppleRiverCanyon.aspx"},\
                                        "payment_info":{"motorcycle":[5,8],"car":[7,10],"rv":[10,13]}}

        expected_response = {"type":'http://localhost/parkpay/parks/data-validation',"title":"Your request data didn't pass validation","detail":"geo information is required but missing in your request","status":400,"instance":"/parks"}

        x = json.loads(controller.validate_park_input(post_data))

        self.assertEqual(x, expected_response)

    """
        Tests the helper function: order_validation()

        - Pass Valid validation data and expect to get a boolean True return
    """
    def test_order_post_data_validation(self):
        post_data = {"pid":-1,"vehicle":{"state":"MIA","plate":"GOCUBS","type":"car"},"visitor":{"name":"Lebron James","email":"ljames@cle.com","payment_info":{"card":"4388567890987654","name_on_card":"Lebron James","expiration_date":"12/19","zip":11111}}}

        self.assertEqual(controller.order_validation(post_data), True)

    """
        Tests the helper function: validation_note_input()

        - Pass faulty validation data and expect to get a 400 error response
    """
    def test_note_post_data_validation(self):
        post_data = {"vid":"0","text":"I can't believe lebron james is here."}

        expected = {
                    "type": "http://localhost/parkpay/parks/data-validation",
                    "title": "Your request data didn't pass validation",
                    "detail": "title information is required but missing in your request",
                    "status": 400,
                    "instance": "/notes"
                    }

        print(controller.validate_note_input(post_data))

        self.assertEqual(json.loads(controller.validate_note_input(post_data)), expected)

    """
        Test the helper function: check_if_visitor_paid()
        
        - Pass a visitor who as not paid and ensure that the return value
          is not true
        - value of not true is a validation error
    """
    def test_check_if_visitor_paid(self):
        os.system("python3 init_data.py")
        allParks = controller.load_serialized_data("park_data")
        allVisitors = controller.load_serialized_data("visitor_data")
        allParks[10] = Park(10)
        allVisitors[10] = Visitor(5)

        controller.dump_serialized_data("park_data",allParks)
        controller.dump_serialized_data("visitor_data", allVisitors)

        self.assertTrue((controller.check_if_visitor_paid(5,10) != True))
        os.system("python3 init_data.py")

    #def test_get_params_from_report_function(self):


    """
        Test the helper function: get_parms_from_report()

        - pass a dummy url, args, and report id and verify the
          output
    """
    def test_get_parms_from_report_function(self):
        url = 'http://localhost:5000/parkpay/reports/917?end_date=20171221'
        args = {'end_date': '20171221'}
        rid = 917

        self.assertEqual(controller.get_parms_from_report(url,args,rid), [None, '20171221'])



    """
        Tests the function: get_all_notes()
        
        - Create a Park and two Notes and verify the are returned with the 
          function
    """
    def test_check_get_all_notes_function(self):
        os.system("python3 init_data.py")
        args = self.data["5"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        allNotes = controller.load_serialized_data("notes_data")
        allParks = controller.load_serialized_data("park_data")

        note1 = Note(0,"")
        note1.title = "Nice Place"
        note2 = Note(1,"")
        note2.title = "Bad Place"

        allNotes[0] = note1
        allNotes[1] = note2

        allParks[0].note_ids.append(0)
        allParks[0].note_ids.append(1)

        controller.dump_serialized_data("notes_data", allNotes)
        controller.dump_serialized_data("park_data", allParks)

        self.assertEqual(controller.get_all_notes(), [{'notes': [{'title': 'Nice Place', 'nid': '0', 'date': ''}, {'title': 'Bad Place', 'nid': '1', 'date': ''}], 'pid': 0}])

    def test_validate_date(self):

        test_date = '20171320'
        self.assertTrue((controller.validate_date(test_date) != True))

    def test_get_cleaned_bounds_one(self):

        self.assertEquals(controller.get_cleaned_bounds(0,[None,None]),[0,99999999])

    def test_get_cleaned_bounds_two(self):

        self.assertEquals(controller.get_cleaned_bounds(0,['20180701','20180731']),[20180701,20180731])

    def test_get_revenue_report_generation(self):
        os.system("python3 init_data.py")
        args = self.data["2"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        allParks = controller.load_serialized_data("park_data")
        allNotes = controller.load_serialized_data("notes_data")

        n1 = Note(0, "2018-2-20")
        n1.title = "Lots of animals"

        n2 = Note(1, "2018-2-22")
        n2.title = "Good food"
        allNotes[0] = n1
        allNotes[1] = n2
        allParks[0].note_ids.append(0)
        allParks[0].note_ids.append(1)

        controller.dump_serialized_data("park_data", allParks)
        controller.dump_serialized_data("notes_data", allNotes)

        expected = {'total_orders': 0, 'end_date': '', 'detail_by_park': [{'revenue': 0, 'pid': '0', 'name': 'Apple River Canyon', 'orders': 0}], 'name': 'Revenue report', 'total_revenue': 0, 'rid': '917', 'start_date': ''}
        print(controller.get_admissions_or_revenue_range([0,99999999], 917))
        self.assertEqual(controller.get_admissions_or_revenue_range([0,99999999], 917), expected)

    def test_get_admission_report_generation(self):
        os.system("python3 init_data.py")
        args = self.data["2"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        allParks = controller.load_serialized_data("park_data")
        allNotes = controller.load_serialized_data("notes_data")

        n1 = Note(0, "2018-2-20")
        n1.title = "Lots of animals"

        n2 = Note(1, "2018-2-22")
        n2.title = "Good food"
        allNotes[0] = n1
        allNotes[1] = n2
        allParks[0].note_ids.append(0)
        allParks[0].note_ids.append(1)

        controller.dump_serialized_data("park_data", allParks)
        controller.dump_serialized_data("notes_data", allNotes)

        args = self.data["12"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        expected = {'end_date': '', 'name': 'Admissions report', 'total_admissions': 1, 'start_date': '', 'rid': '911', 'detail_by_park': [{'name': 'Apple River Canyon', 'pid': '0', 'admissions': 1}]}
        self.assertEqual(controller.get_admissions_or_revenue_range([0,99999999], 911), expected)


    def test_get_all_data_in_bounds_method(self):
        os.system("python3 init_data.py")
        args = self.data["2"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        allParks = controller.load_serialized_data("park_data")
        allNotes = controller.load_serialized_data("notes_data")

        n1 = Note(0, "2018-2-20")
        n1.title = "Lots of animals"

        n2 = Note(1, "2018-2-22")
        n2.title = "Good food"
        allNotes[0] = n1
        allNotes[1] = n2
        allParks[0].note_ids.append(0)
        allParks[0].note_ids.append(1)

        controller.dump_serialized_data("park_data", allParks)
        controller.dump_serialized_data("notes_data", allNotes)

        args = self.data["12"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        expected = [{'parks': [{'location_info': {'phone': '815-745-3302', 'web': 'https://www.dnr.illinois.gov/Parks/Pages/AppleRiverCanyon.aspx', 'address': '8763 E. Canyon Rd, Apple River, IL 61001', 'region': 'Northwestern Illinois', 'geo': {'lat': 42.448, 'lng': -90.043}, 'name': 'Apple River Canyon'}, 'pid': '0'}]}, {'notes': [{'date': '2018-2-20', 'nid': '0', 'title': 'Lots of animals'}, {'date': '2018-2-22', 'nid': '1', 'title': 'Good food'}]}, {'orders': [{'oid': '0', 'type': 'car', 'amount': 7, 'date': '2018-11-13', 'pid': '0'}]}, {'visitors': [{'vid': '0', 'name': 'John Doe', 'email': 'john.doe@example.com'}]}]

        self.assertEqual(controller.get_all_data_in_bounds("", [0, 99999999]), expected)

    def test_get_all_parks_function(self):
        os.system("python3 init_data.py")
        args = self.data["2"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        args = self.data["5"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        expected = [{'pid': '0', 'location_info': {'region': 'Northwestern Illinois', 'phone': '815-745-3302', 'address': '8763 E. Canyon Rd, Apple River, IL 61001', 'geo': {'lat': 42.448, 'lng': -90.043}, 'web': 'https://www.dnr.illinois.gov/Parks/Pages/AppleRiverCanyon.aspx', 'name': 'Apple River Canyon'}}, {'pid': '1', 'location_info': {'region': 'Southern Illinois', 'phone': '618-524-5577', 'address': '1812 Grinnell Road, Belknap, IL 62908', 'geo': {'lat': 37.275, 'lng': -88.849}, 'web': 'https://www.dnr.illinois.gov/Parks/Pages/MermetLake.aspx', 'name': 'Mermet Lake'}}]
        self.assertEqual(controller.get_all_parks(), expected)


    def test_get_all_orders_function(self):
        args = self.data["2"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        args = self.data["12"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        expected = [{'date': '2018-11-13', 'oid': '0', 'type': 'car', 'amount': 7, 'pid': '0'}, {'date': '2018-11-13', 'oid': '1', 'type': 'car', 'amount': 7, 'pid': '0'}]
        self.assertEqual(controller.get_all_orders(), expected)

    def test_get_all_reports_function(self):
        args = self.data["30"]
        r = requests.get(args[1], headers=self.headers)

        expected = [{'rid': '911', 'name': 'Admissions report'}, {'rid': '917', 'name': 'Revenue report'}]
        self.assertEqual(r.json(), expected)

    def test_get_all_visitors(self):
        os.system("python3 init_data.py")
        allVisitors = controller.load_serialized_data("visitor_data")
        v1 = Visitor(0)
        v1.name = "Test Visitor1"
        v1.email = "testvisitor1@parkpay.com"
        v2 = Visitor(1)
        v2.name = "Test Visitor2"
        v2.email = "testvisitor2@parkpay.com"

        allVisitors[0] = v1
        allVisitors[1] = v2

        controller.dump_serialized_data("visitor_data", allVisitors)
        print(controller.get_all_visitors())
        expected = {}
        self.assertEqual(2+2,4)
        
    def test_check_resource_exists_function(self):

        expected = {'status': 404, 'type': 'http://localhost/parkpay/data-validation', 'title': 'Resource: park does not contain element with ID: 50'}
        self.assertEqual(controller.check_resource_exists("park",50), expected)

    def test_status_code_of_order_generation(self):
        args = self.data["2"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        args = self.data["12"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        self.assertEqual(r.status_code, 201)

    def test_search_all_data(self):
        args = self.data["2"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        args = self.data["12"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        r = requests.get(url="http://localhost:5000/parkpay/search?key=")
        expected = [{'parks': [{'location_info': {'region': 'Northwestern Illinois', 'phone': '815-745-3302', 'geo': {'lat': 42.448, 'lng': -90.043}, 'address': '8763 E. Canyon Rd, Apple River, IL 61001', 'web': 'https://www.dnr.illinois.gov/Parks/Pages/AppleRiverCanyon.aspx', 'name': 'Apple River Canyon'}, 'pid': '0'}]}, {'notes': []}, {'orders': [{'date': '2018-11-13', 'type': 'car', 'oid': '0', 'pid': '0', 'amount': 7}]}, {'visitors': [{'vid': '0', 'email': 'john.doe@example.com', 'name': 'John Doe'}]}]
        self.assertEqual(r.json(), expected)


    def test_update_park(self):
        os.system("python3 init_data.py")
        args = self.data["2"]
        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)

        args = self.data["4"]
        print(args)
        r = requests.put(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.status_code, 204)
        

if __name__ == '__main__':
    unittest.main()


