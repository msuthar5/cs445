from flask import Flask, request, make_response #, json, Response
from core.order import *
from core.note import *
from core.park import *
from core.report import *
from core.visitor import *
from utilities.utils import *
import pickle
import json
import datetime

import functools
app = Flask(__name__)

ADMISSIONS = 911
REVENUE = 917


def get_cleaned_bounds(rid, date_range):

    start_date = None
    end_date = None
    if date_range[0] == None:
        if date_range[1] != None:
            end_date = int(date_range[1])
        else:
            end_date = 99999999
        start_date = 0
    elif date_range[0] != None:
        start_date = int(date_range[0])
        if date_range[1] == None:
            end_date = 99999999
        else:
            end_date = int(date_range[1])

    return [start_date, end_date]


def get_all_data_in_bounds(keyword, bounds):

    allParks = load_serialized_data("park_data")
    allNotes = load_serialized_data("notes_data")
    allOrders = load_serialized_data("order_data")
    allVisitors = load_serialized_data("visitor_data")

    return_obj = [None,None,None,None]
    return_obj[0] = {"parks": []}
    return_obj[1] = {"notes": []}
    return_obj[2] = {"orders": []}
    return_obj[3] = {"visitors": []}

    for k,v in allParks.items():
        if k != "id":
            if keyword.lower() in str(v.toJsonObject(True)).lower():
                return_obj[0]["parks"].append(v.toJsonObject(False))

    for k,v in allNotes.items():
        if k != "id":
            if keyword.lower() in v.title.lower() or keyword.lower() in v.text.lower():
                if int(v.date.replace("-", "")) in range(bounds[0], bounds[1]):
                    return_obj[1]["notes"].append(v.getAsJsonObject())

    for k, v in allOrders.items():
        if k != "id":
            order = v
            visitor = allVisitors[order.visitor_id]
            if keyword.lower() in str(visitor.vehicle).lower() or \
                            keyword.lower() in str(visitor.payment_info).lower() or \
                            keyword.lower() in order.date or keyword.lower() in str(order.amount):
                if int(order.date.replace("-", "")) in range(bounds[0], bounds[1]):
                    return_obj[2]["orders"].append(order.getAsJsonObject())

    for k,v in allVisitors.items():
        if k != "id":
            if keyword.lower() in str(v.vid) or keyword.lower() in v.name.lower() or keyword.lower() in v.email.lower():
                return_obj[3]["visitors"].append(v.getSimpleJsonObject())

    return return_obj


def get_admissions_or_revenue_range(bounds, type):

    report = None
    start_date = bounds[0]
    end_date = bounds[1]
    allReports = load_serialized_data("report_data")
    allParks = load_serialized_data("park_data")
    allOrders = load_serialized_data("order_data")

    if type == REVENUE:
        report = allReports[str(REVENUE)]
    else:
        report = allReports[str(ADMISSIONS)]

    for k, v in allParks.items():
        if k != "id":
            obj = {}
            if type == REVENUE:
                obj["pid"] = str(k)
                obj["name"] = v.name
                obj["revenue"] = 0
                obj["orders"] = 0
            else:
                obj["pid"] = str(k)
                obj["name"] = v.name
                obj["admissions"] = 0

            for id, order in allOrders.items():
                if id != "id":
                    if order.park_id == k:
                        date = order.date.replace("-","")
                        if int(date) in range(int(start_date),int(end_date)):
                            if type == REVENUE:
                                report.total_orders += 1
                                report.total_revenue += float(order.amount)
                                obj["orders"] += 1
                                obj["revenue"] += float(order.amount)
                            else:
                                obj["admissions"] += 1
                                report.total_admissions += 1
            report.detail_by_park.append(obj)
            if start_date != 0:
                report.start_date = str(start_date)[:4] + '-' + str(start_date)[4:6] + '-' + str(start_date)[6:]
            if end_date != 99999999:
                report.end_date = str(end_date)[:4] + '-' + str(end_date)[4:6] + '-' + str(end_date)[6:]
    return report.getAsJsonObject()


def validate_date(date):
    error = {
            "type": "http://localhost/parkpay/parks/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "Wrong date format",
            "status": 400,
            "instance": "/reports/917"
        }
    if len(date) != 8:
        return error
    try:
        d = datetime.datetime(year=int(date[:4]), month=int(date[4:6]), day=int(date[6:]))
    except:
        return error
    return True


def order_validation(req):

    error = {
        "type": "http://localhost/parkpay/orders/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": 0,
        "status": 400,
        "instance": "/orders"
    }

    keys = ['pid', 'vehicle', 'visitor']
    vehicle_keys = ['state', 'plate', 'type']
    visitor_keys = ['name', 'email', 'payment_info']
    payment_keys = ['card', 'name_on_card', 'expiration_date', 'zip']

    for k in keys:
        if k not in req.keys():
            error["detail"] = "{} information is missing".format(k)
            return error

    for vk in vehicle_keys:
        if vk not in req["vehicle"].keys():
            error["detail"] = "{} information is missing".format(vk)
            return error

    for visitkey in visitor_keys:
        if visitkey not in req["visitor"].keys():
            error["detail"] = "{} information is missing".format(visitkey)
            return error

    for paykey in payment_keys:
        if paykey not in req["visitor"]["payment_info"]:
            error["detail"] = "{} information is missing".format(paykey)
            return error

    if req["pid"] != -1:
        allParks = load_serialized_data("park_data")
        if int(req["pid"]) not in allParks.keys():
            error["detail"] = "Park with ID: {} does not exist".format(str(req["pid"]))
            return error
    return True


def get_parms_from_report(url, args, rid):
    start_date = args.get("start_date")
    end_date = args.get("end_date")

    id_len = len(str(rid))
    # check for end_date parameter
    if len(url) > (59+id_len):
        return [start_date, url[68+id_len:]]
        end_date = url[68+id_len:]
    return [start_date, end_date]

def resource_not_found(resource, id):
    error = {
        "type": "http://localhost/parkpay/parks/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": "Resource: {} has no entry for ID: {}".format(resource, str(id)),
        "status": 404,
        "instance": "/" + resource
    }
    return error

def get_all_parks():

    allParks = load_serialized_data("park_data")
    return_obj = []
    for k, v in allParks.items():
        if k != "id":
            return_obj.append(v.toJsonObject(False))
    return return_obj


def get_all_notes():
    allNotes = load_serialized_data("notes_data")
    allParks = load_serialized_data("park_data")
    return_obj = []
    for k, v in allParks.items():
        if k != "id":
            if len(allParks[k].note_ids) > 0:
                element = {}
                element["pid"] = k
                element["notes"] = []
                for note_id in allParks[k].note_ids:
                    element["notes"].append(allNotes[note_id].getAsJsonObject())
                return_obj.append(element)

    return return_obj


def get_all_orders():
    allOrders = load_serialized_data("order_data")

    return_obj = []
    for k, v in allOrders.items():
        if k != "id":
            return_obj.append(v.getAsJsonObject())

    return return_obj


def get_all_visitors():
    return_obj = []
    allVisitors = load_serialized_data("visitor_data")
    for k, v in allVisitors.items():
        if k != "id":
            return_obj.append(v.getSimpleJsonObject())
    return return_obj


def validate_note_input(request_data):
    error = {
        "type": "http://localhost/parkpay/parks/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": "",
        "status": 400,
        "instance": "/notes"
    }

    required = ["vid", "title", "text"]
    for req in required:
        if req not in request_data.keys():
            error["detail"] = "{} information is required but missing in your request".format(req)
            return json.dumps(error)
    return None

@app.route('/parkpay/reports/<int:rid>', methods=['GET'])
def report_generator(rid):
    if len(request.args) > 0:
        date_range = get_parms_from_report(request.url, request.args, rid)

        for a in date_range:
            if a:
                validation = validate_date(a)
                if validation != True:
                    return make_response(json.dumps(validation),400)

        #return json.dumps(date_range)
        cleaned_bounds = get_cleaned_bounds(rid, date_range)
        return_obj = get_admissions_or_revenue_range(cleaned_bounds,rid)
        return make_response(json.dumps(return_obj), 200)

    cleaned_bounds = [0, 99999999]
    return_obj = get_admissions_or_revenue_range(cleaned_bounds, rid)
    return make_response(json.dumps(return_obj), 200)

@app.route('/parkpay/reports', methods=['GET'])
def return_all_reports():
    return_obj = []
    allReports = load_serialized_data("report_data")
    for k,v in allReports.items():
        if k != "id":
            return_obj.append(v.getSimpleJsonObject())
    return make_response(json.dumps(return_obj), 200)

def validate_park_input(request_data):
    error = {
        "type": "http://localhost/parkpay/parks/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": "",
        "status": 400,
        "instance": "/parks"
    }

    required = ["location_info", "payment_info"]
    required_loc = ["name", "geo", "address", "phone", "web", "region"]
    required_payment = ["motorcycle", "car", "rv"]

    for i in required:
        if i not in request_data.keys():
            error["detail"] = "{} information is required but missing in your request".format(i)
            return json.dumps(error)

    for key in required_loc:
        if key not in request_data["location_info"].keys():
            error["detail"] = "{} information is required but missing in your request".format(key)
            return json.dumps(error)

    for k in required_payment:
        if k not in request_data["payment_info"].keys():
            error["detail"] = "{} information is required but missing in your request".format(k)
            return json.dumps(error)

    for vehicle in request_data['payment_info'].keys():
        prices = request_data['payment_info'][vehicle]
        if prices[0] < 0 or prices[1] < 0:
            error["detail"] = "All payment data must be a number greater than or equal to zero"
            return json.dumps(error)
    return None

@app.route('/parkpay/parks', methods=['GET', 'POST'])
def create_park():
    allParks = load_serialized_data("park_data")
    if request.method == 'POST':

        validation = validate_park_input(request.json)
        if validation is not None:
            return make_response(validation, 400)

        # Create Park object
        pid = allParks["id"]

        park = Park(pid)
        park.name = request.json['location_info']['name']
        park.address = request.json['location_info']['address']
        park.phone = request.json['location_info']['phone']
        park.web = request.json['location_info']['web']
        park.region = request.json['location_info']['region']
        park.payment_info['motorcycle'] = request.json['payment_info']['motorcycle']
        park.payment_info['car'] = request.json['payment_info']['car']
        park.payment_info['rv'] = request.json['payment_info']['rv']
        park.geo = request.json['location_info']['geo']

        allParks["id"] = pid + 1
        allParks[pid] = park

        dump_serialized_data("park_data", allParks)

        return make_response(json.dumps({"pid": str(park.pid)}), 201)
    else:

        if len(request.args) > 0:
            query = request.args["key"]
            if query == "":
                return json.dumps(get_all_parks())
            return_obj = []
            for k,v in allParks.items():
                if k != "id":
                    if query.lower() in v.name.lower() or \
                       query.lower() in v.region.lower() or \
                       query.lower() in v.address.lower():

                        return_obj.append(v.toJsonObject(False))

            return make_response(json.dumps(return_obj), 200)

        return_obj = get_all_parks()

        return make_response(json.dumps(return_obj), 200)


def check_resource_exists(resource, id):

    allData = load_serialized_data(resource+"_data")

    if int(id) not in allData.keys():
        return {"type": "http://localhost/parkpay/data-validation",
                "title": "Resource: {} does not contain element with ID: {}".format(resource, id),
                "status": 404}
    return True


def check_if_visitor_paid(vid,pid):
    allOrders = load_serialized_data("order_data")
    paid = False
    for k,v in allOrders.items():
        if k != "id":
            if str(v.visitor_id) == str(vid) and str(v.park_id) == str(pid):
                paid = True

    if paid == False:
        return {
                  "type": "http://localhost/parkpay/parks/data-validation",
                  "title": "Your request data didn't pass validation",
                  "detail": "You may not post a note to a park unless you paid for admission at that park",
                  "status": 400,
                  "instance": "/parks/" + str(pid)
                }
    return True


@app.route('/parkpay/parks/<int:park_id>/notes', methods=['GET', 'POST'])
def get_or_create_note(park_id):

    allParks = load_serialized_data("park_data")
    allNotes = load_serialized_data("notes_data")

    if request.method == 'POST':

        validation = validate_note_input(request.json)
        if validation is not None:
            return make_response(validation, 400)

        does_exist = check_resource_exists("park", park_id)
        if does_exist != True:
            return make_response(json.dumps(does_exist), 400)

        has_user_paid = check_if_visitor_paid(request.json["vid"], park_id)
        if has_user_paid != True:
            return make_response(json.dumps(has_user_paid), 400)

        park = allParks[int(park_id)]
        nid = allNotes["id"]
        note = Note(nid, datetime.date.today().strftime("%Y-%m-%d"))
        note.visitor_id = request.json["vid"]
        note.title = request.json["title"]
        note.park_id = park_id
        note.text = request.json["text"]
        park.note_ids.append(nid)

        allNotes["id"] = nid + 1
        allNotes[nid] = note
        allParks[park_id] = park

        dump_serialized_data("notes_data", allNotes)
        dump_serialized_data("park_data", allParks)

        return make_response(json.dumps({"nid": str(nid)}), 201)

    else:

        does_exist = check_resource_exists("park", park_id)

        if does_exist != True:
            return make_response(json.dumps(does_exist), 404)

        park = allParks[park_id]
        return_obj = [None]
        return_obj[0] = {"pid": str(park_id), "notes": []}
        for nid in park.note_ids:
            return_obj[0]["notes"].append(allNotes[nid].getAsJsonObject())

        return make_response(json.dumps(return_obj), 200)

@app.route('/parkpay/notes/<int:note_id>', methods=['GET', 'DELETE', 'PUT'])
def get_single_note(note_id):

    allParks = load_serialized_data("park_data")
    allNotes = load_serialized_data("notes_data")

    does_note_exist = check_resource_exists("notes", note_id)
    if does_note_exist != True:
        return make_response(json.dumps(does_note_exist),404)

    note = allNotes[note_id]
    park = allParks[note.park_id]
    if request.method == "GET":

        return make_response(json.dumps({"vid": note.visitor_id,
                           "pid": str(note.park_id),
                           "nid": str(note_id),
                           "date": note.date,
                           "title": note.title,
                           "text": note.text}), 200)

    elif request.method == "DELETE":

        del allNotes[note_id]

        park.note_ids.remove(note_id)

        dump_serialized_data("notes_data", allNotes)
        dump_serialized_data("park_data", allParks)

        return make_response(json.dumps({}), 204)

    elif request.method == 'PUT':

        validation = validate_note_input(request.json)
        if validation is not None:
            return make_response(validation, 400)

        note.visitor_id = request.json["vid"]
        note.title = request.json["title"]
        note.text = request.json["text"]

        allNotes[note_id] = note

        dump_serialized_data("notes_data", allNotes)

        return make_response(json.dumps({}), 204)

@app.route('/parkpay/notes', methods=['GET'])
def return_all_notes():
    if len(request.args) > 0:

        allParks = load_serialized_data("park_data")
        query = request.args["key"]
        if query == "":
            return make_response(json.dumps(get_all_notes()),200)
        return_obj = []
        allNotes = load_serialized_data("notes_data")
        for k,v in allParks.items():
            if k != "id":
                obj = {}
                obj["pid"] = k
                obj["notes"] = []

                for note_id in v.note_ids:
                    note = allNotes[note_id]
                    if query.lower() in note.title.lower() or query.lower() in note.text.lower():
                        obj["notes"].append(note.getAsJsonObject())
                if len(obj["notes"]) > 0:
                    return_obj.append(obj)
        return make_response(json.dumps(return_obj), 200)
    return make_response(json.dumps(get_all_notes()), 200)

@app.route('/parkpay/parks/<int:park_id>/notes/<int:note_id>', methods=['GET', 'DELETE'])
def view_single_note(park_id, note_id):

    does_park_exist = check_resource_exists("park",park_id)
    does_note_exist = check_resource_exists("notes", note_id)

    if does_park_exist != True:
        return make_response(json.dumps(does_park_exist), 404)
    if does_note_exist != True:
        return make_response(json.dumps(does_note_exist), 404)

    allParks = load_serialized_data("park_data")
    allNotes = load_serialized_data("notes_data")

    if note_id not in allParks[park_id].note_ids:
        return make_response(json.dumps({
                "type": "http://localhost/parkpay/parks/data-validation",
                "detail": "Note with ID: {} is not associated with the park having ID: {}".format(note_id, park_id),
                "status": 400
                }), 400)

    if request.method == "GET":
        note = allNotes[note_id]

        return make_response(json.dumps({"vid": note.visitor_id,
                           "pid": str(park_id),
                           "nid": str(note_id),
                           "date": note.date,
                           "title": note.title,
                           "text": note.text}), 200)

@app.route('/parkpay/orders/<int:order_id>', methods=['GET', 'DELETE'])
def get_single_order(order_id):

    allOrders = load_serialized_data("order_data")
    if int(order_id) not in allOrders.keys():
        return make_response(json.dumps(resource_not_found("orders", order_id)), 404)
    if request.method == "GET":

        order = allOrders[order_id]
        allVisitors = load_serialized_data("visitor_data")
        visitor = allVisitors[order.visitor_id]

        return_obj = order.getVerboseJsonObject()
        return_obj["vehicle"] = visitor.vehicle
        return_obj["visitor"] = visitor.getAsJsonObject()

        return make_response(json.dumps(return_obj), 200)



@app.route('/parkpay/orders', methods=['GET', 'POST'])
def order_handler():

    allOrders = load_serialized_data("order_data")

    if request.method == "POST":

        validation = order_validation(request.json)
        if validation != True:
            print("HEYEYEYEYEYYE")
            return make_response(json.dumps(validation), 400)

        does_park_exist = check_resource_exists("park", request.json["pid"])

        if does_park_exist != True:
            print(str(request.json["pid"]))
            return make_response(json.dumps(does_park_exist), 400)

        allOrders = load_serialized_data("order_data")
        allVisitors = load_serialized_data("visitor_data")
        allParks = load_serialized_data("park_data")
        allVehicles = load_serialized_data("vehicle_data")
        visitor = None

        for k,v in allVisitors.items():
            if k != "id":
                if v.email == request.json["visitor"]["email"]:
                    visitor = v

        if visitor == None:

            visitor = Visitor(allVisitors["id"])

            if len(request.json["visitor"]["name"]) == 0:
                visitor.name = request.json["visitor"]["payment_info"]["name_on_card"]
            else:
                visitor.name = request.json["visitor"]["name"]

            visitor.email = request.json["visitor"]["email"]
            visitor.payment_info = build_payment_information(request.json["visitor"]["payment_info"]["card"],
                                                             request.json["visitor"]["payment_info"]["name_on_card"],
                                                             request.json["visitor"]["payment_info"]["expiration_date"],
                                                             request.json["visitor"]["payment_info"]["zip"])

            visitor.vehicle = build_vehicle_information(allVisitors["id"],
                                                        request.json["vehicle"]["state"],
                                                        request.json["vehicle"]["plate"],
                                                        request.json["vehicle"]["type"])

            allVisitors["id"] += 1
            allVisitors[visitor.vid] = visitor
            dump_serialized_data("visitor_data", allVisitors)


        order = Order(allOrders["id"])
        order.type = request.json["vehicle"]["type"]
        order.date = datetime.date.today().strftime("%Y-%m-%d")
        order.visitor_id = visitor.vid
        order.park_id = request.json["pid"]
        order.payment_processing["card_transaction_id"] = generate_transaction_id()
        order.payment_processing["date_and_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        park = allParks[int(request.json["pid"])]

        if visitor.vehicle["state"] in park.address:
            order.amount = park.payment_info[visitor.vehicle["type"]][0]
        else:
            order.amount = park.payment_info[visitor.vehicle["type"]][1]

        allOrders[order.oid] = order
        allOrders["id"] += 1
        #allVisitors["id"] += 1
        #allVisitors[visitor.vid] = visitor

        dump_serialized_data("order_data", allOrders)
        #dump_serialized_data("visitor_data", allVisitors)

        return make_response(json.dumps({"oid": str(order.oid)}), 201)

    elif request.method == "GET":

        allVisitors = load_serialized_data("visitor_data")

        if len(request.args) > 0:
            query = request.args["key"]
            if query == "":
                return make_response(json.dumps(get_all_orders()), 200)
            return_obj = []
            for k,v in allOrders.items():
                if k != "id":
                    order = v
                    print(order.visitor_id)
                    visitor = allVisitors[int(order.visitor_id)]
                    if query.lower() in str(visitor.vehicle).lower() or \
                       query.lower() in str(visitor.payment_info).lower() or \
                       query.lower() in order.date or query.lower() in str(order.amount):
                        return_obj.append(order.getAsJsonObject())

            return make_response(json.dumps(return_obj), 200)

        return make_response(json.dumps(get_all_orders()), 200)


@app.route('/parkpay/parks/<int:park_id>', methods=['PUT', 'GET'])
def update_park(park_id):

    allParks = load_serialized_data("park_data")
    if park_id not in allParks.keys():
        err = {
            "type": "http://localhost/parkpay/parks/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "park with id: {} does not exist".format(park_id),
            "status": 404,
            "instance": "/parks/" + park_id
        }
        return make_response(json.dumps(err), 404)

    park = allParks[park_id]

    if request.method == "PUT":

        validation = validate_park_input(request.json)
        if validation is not None:
            return make_response(validation, 400)

        park.name = request.json['location_info']['name']
        park.address = request.json['location_info']['address']
        park.phone = request.json['location_info']['phone']
        park.web = request.json['location_info']['web']
        park.region = request.json['location_info']['region']
        park.payment_info['motorcycle'] = request.json['payment_info']['motorcycle']
        park.payment_info['car'] = request.json['payment_info']['car']
        park.payment_info['rv'] = request.json['payment_info']['rv']
        park.geo = request.json['location_info']['geo']

        allParks[park_id] = park

        dump_serialized_data("park_data", allParks)

        return make_response(json.dumps(""), 204)
    elif request.method == "GET":

        return make_response(json.dumps(park.toJsonObject(True)), 200)

@app.route('/parkpay/parks/<int:park_id>', methods=['DELETE'])
def delete_park(park_id):

    allParks = load_serialized_data("park_data")
    if park_id not in allParks.keys():
        return make_response("", 404)

    # deleting the park
    del allParks[park_id]
    dump_serialized_data("park_data", allParks)

    return make_response(json.dumps({}), 204)

@app.route('/parkpay/visitors', methods=['GET'])
def return_all_visitors():

    if len(request.args) > 0:
        allVisitors = load_serialized_data("visitor_data")
        query = request.args["key"]
        if query == "":
            return json.dumps(get_all_visitors())
        return_obj = []
        for k,v in allVisitors.items():
            if k != "id":
                if query.lower() in str(v.vid) or query.lower() in v.name.lower() or query.lower() in v.email.lower():
                    return_obj.append(v.getSimpleJsonObject())
        return json.dumps(return_obj)

    return make_response(json.dumps(get_all_visitors()), 200)

@app.route('/parkpay/visitors/<int:visitor_id>', methods=['GET'])
def get_single_visitor(visitor_id):
    does_exist = check_resource_exists("visitor", visitor_id)
    if does_exist != True:
        return make_response(json.dumps(does_exist),404)

    allVisitors = load_serialized_data("visitor_data")
    allOrders = load_serialized_data("order_data")
    allNotes = load_serialized_data("notes_data")
    visitor = allVisitors[visitor_id]

    return_obj = {}
    return_obj["vid"] = str(visitor_id)
    return_obj["visitor"] = {}
    return_obj["visitor"]["name"] = visitor.name
    return_obj["visitor"]["email"] = visitor.email
    return_obj["orders"] = []
    return_obj["notes"] = []
    for k,v in allOrders.items():
        if k != "id":
            order = v
            obj = {}
            if order.visitor_id == visitor_id:
                obj["oid"] = str(order.oid)
                obj["pid"] = str(order.park_id)
                obj["date"] = order.date
                return_obj["orders"].append(obj)

    for key,val in allNotes.items():
        if key != "id":
            note = val
            obj = {}
            if str(note.visitor_id) == str(visitor_id):
                obj["nid"] = str(note.nid)
                obj["pid"] = str(note.park_id)
                obj["date"] = note.date
                obj["title"] = note.title
                return_obj["notes"].append(obj)

    return make_response(json.dumps(return_obj), 200)


@app.route('/parkpay/search', methods=['GET'])
def search():
    if len(request.args) > 0:
        key = request.args.get("key")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if key:
            key = key.replace("{","")
        else:
            key = ""
        if end_date:
            end_date = end_date.replace("}", "")
        cleaned_bounds = get_cleaned_bounds(0, [start_date, end_date])
        return make_response(json.dumps(get_all_data_in_bounds(key,cleaned_bounds)), 200)
    return json.dumps(get_all_data_in_bounds("", [0,99999999]))

def load_serialized_data(file_name):
    f = open("data_storage/" + file_name, "rb")
    obj = f.read()
    f.close()
    return pickle.loads(obj)


def dump_serialized_data(file_name, to_ser):
    f = open("data_storage/" + file_name, "wb")
    f.write(pickle.dumps(to_ser))
    f.close()

if __name__ == '__main__':
    app.run(debug=True)