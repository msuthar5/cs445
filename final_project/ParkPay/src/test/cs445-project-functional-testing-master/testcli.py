import json, re
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/parkpay'

# 18, 31
tests = [
    # ('GET', <path>, <status_code>, <expected_response>[, <list_of_new_ids>]),
    # ('POST', <path>, <request>, <status_code>, <expected_response>[, <new_id>]),
    # ('PUT', <path>, <request>, <status_code>[, <expected_response>]),
    # ('DELETE', <path>, <status_code>),

    ('GET', '/parks', 200, []),
    ('POST', '/parks', 'test-data/test-parks-create-POST-1.json', 400, 'test-data/test-parks-create-POST-1-response.json'),
    ('POST', '/parks', 'test-data/test-parks-create-POST-2.json', 201, 'test-data/test-parks-create-POST-2-response.json', '{pid1}'),
    ('GET', '/parks/{pid1}', 200, 'test-data/test-parks-view-park-detail-GET-1-response.json'),
    ('PUT', '/parks/{pid1}', 'test-data/test-parks-update-PUT-1.json', 204),
    
    ('POST', '/parks', 'test-data/test-parks-create-POST-3.json', 201, 'test-data/test-parks-create-POST-3-response.json', '{pid2}'),
    ('POST', '/parks', 'test-data/test-parks-create-POST-4.json', 201, 'test-data/test-parks-create-POST-4-response.json', '{pid3}'),
    ('GET', '/parks', 200, 'test-data/test-parks-view-GET-1-response.json'),
    ('GET', '/parks?key=south', 200, 'test-data/test-parks-view-GET-3-response.json'),
    ('DELETE', '/parks/{pid2}', 204),

    ('DELETE', '/parks/{pid2}', 404),
    ('GET', '/parks?key=', 200, 'test-data/test-parks-view-GET-2-response.json'),
    ('POST', '/orders', 'test-data/test-orders-create-POST-1.json', 201, 'test-data/test-orders-create-POST-1-response.json', '{oid1}'),
    ('GET', '/orders', 200, 'test-data/test-orders-view-GET-1-response.json'),
    ('GET', '/visitors', 200, 'test-data/test-visitors-view-GET-1-response.json', ['{vid1}']),

    ('GET', '/visitors/{vid1}', 200, 'test-data/test-visitors-view-visitor-detail-GET-1-response.json'),
    ('POST', '/parks/{pid1}/notes', 'test-data/test-parks-create-note-POST-1.json', 400, 'test-data/test-parks-create-note-POST-1-response.json'),
    ('POST', '/parks/{pid3}/notes', 'test-data/test-parks-create-note-POST-2.json', 201, 'test-data/test-parks-create-note-POST-2-response.json', '{nid1}'),
    ('GET', '/visitors/{vid1}', 200, 'test-data/test-visitors-view-visitor-detail-GET-2-response.json'),
    ('GET', '/notes/{nid1}', 200, 'test-data/test-notes-view-note-detail-GET-1-response.json'),

    ('POST', '/orders', 'test-data/test-orders-create-POST-2.json', 201, 'test-data/test-orders-create-POST-2-response.json', '{oid2}'),
    ('POST', '/orders', 'test-data/test-orders-create-POST-3.json', 201, 'test-data/test-orders-create-POST-3-response.json', '{oid3}'),
    ('GET', '/visitors', 200, 'test-data/test-visitors-view-GET-2-response.json', ['{vid1}', '{vid2}']),
    ('POST', '/parks/{pid3}/notes', 'test-data/test-parks-create-note-POST-3.json', 201, 'test-data/test-parks-create-note-POST-3-response.json', '{nid2}'),
    ('GET', '/parks/{pid3}/notes', 200, 'test-data/test-parks-view-notes-GET-1-response.json'),

    ('GET', '/parks/{pid3}/notes/{nid2}', 200, 'test-data/test-notes-view-note-detail-GET-2-response.json'),
    ('GET', '/orders/{oid3}', 200, 'test-data/test-orders-view-order-detail-GET-1-response.json'),
    ('GET', '/orders', 200, 'test-data/test-orders-view-GET-2-response.json'),
    ('GET', '/orders?key=60MPG', 200, 'test-data/test-orders-search-GET-1-response.json'),
    ('GET', '/visitors?key=john', 200, 'test-data/test-visitors-search-GET-1-response.json'),

    ('GET', '/reports', 200, 'test-data/test-reports-GET-1-response.json', ['{rid1}', '{rid2}']),
    ('GET', '/reports/{rid1}', 200, 'test-data/test-reports-admissions-GET-1-response.json'),
    ('GET', '/reports/{rid1}?end_date=20171231', 200, 'test-data/test-reports-admissions-GET-2-response.json'),
    ('GET', '/reports/{rid2}', 200, 'test-data/test-reports-revenue-GET-1-response.json'),
    ('GET', '/reports/{rid2}?end_date=20171232', 400, 'test-data/test-reports-revenue-GET-2-response.json')
]

def orderize(obj):
    """
    Orderize the json object for comparison.
    """
    if isinstance(obj, dict):
        return sorted((k, orderize(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return sorted(orderize(x) for x in obj)
    return obj

class ParkpayTestClient:
    """
    The class created for the testing of the Parkpay server.
    """

    def __init__(self, url, tests):
        """
        Initialization.

        :param url: the base URL.
        :param tests: a list of test cases.
        """
        self.baseurl = url
        self.tests = tests
        self.date_str = datetime.now().strftime('%Y-%m-%d')

        self.reo_1 = re.compile(r'{[^{]+}')
        self.reo_2 = re.compile(r'<([^<]+)>')
        self.reo_i = re.compile(r'.id')
        self.ids = {}

        self.post_cases = [
            (r'/parks$', 'pid'),
            (r'/orders$', 'oid'),
            (r'/parks/[^/]+/notes$', 'nid'),
        ]
        self.get_cases = [
            (r'/visitors$', 'vid'),
            (r'/reports$', 'rid'),
        ]

    def f2o(self, obj):
        """
        Load the json object from a file.

        :param obj: either a json object or a path to a json file.
        """
        if isinstance(obj, str):
            with open(obj, 'r') as f:
                return json.load(f)
        return obj

    def replace_ids_in_path(self, path):
        """
        Replace the ID tabs in the request URL with real IDs.
        
        :param path: the subpath in the request URL.
        :return: the new path string.
        """
        m = self.reo_1.search(path)
        while m:
            if m.group(0) not in self.ids:
                return None
            print(m)
            path = path[:m.start()] + self.ids[m.group(0)] + path[m.end():]
            m = self.reo_1.search(path)
        return path

    def replace_ids_in_req(self, msg):
        """
        Replace the ID tabs in the request message (json object) with real IDs.
        
        :param msg: the request message represented by a json object.
        :return: the new json object.
        """
        for k, v in msg.items():
            if self.reo_i.match(k):
                m = self.reo_2.match(v)
                msg[k] = self.ids['{%s}' % (m.group(1))]
        return msg

    def replace_ids_in_res(self, obj):
        """
        Replace the ID tabs in the response message (json object) with real IDs.

        :param obj: the response json object.
        :return: the new json object.
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if self.reo_i.match(k):
                    m = self.reo_2.match(v)
                    obj[k] = self.ids['{%s}' % (m.group(1))]
                else:
                    obj[k] = self.replace_ids_in_res(v)
        elif isinstance(obj, list):
            return [self.replace_ids_in_res(o) for o in obj]
        elif isinstance(obj, str):
            if re.match(r'<date.+id.+>$', obj):
                obj = self.date_str
        return obj

    def check_response_400(self, resj, path):
        """
        Check the response json object of status code 400.
        """
        if 'status' not in resj or resj['status'] != 400 or \
           'instance' not in resj or \
           'type' not in resj or 'title' not in resj or 'detail' not in resj:
            print('Unexpected response for status 400:\n%s' % (resj))
            return False
        return True


    def run(self):
        """
        Run the tests. Stop on failure.
        """
        methods = {
            'GET': self.test_get,
            'POST': self.test_post,
            'PUT': self.test_put,
            'DELETE': self.test_delete,
        }

        for i in range(len(self.tests)):
            if methods[self.tests[i][0]](self.tests[i]):
                print('Test %d passed' % (i+1))
            else:
                print('Failed on the test:')
                print(self.tests[i])
                #break


    def test_get(self, tinfo):
        """
        Test a "GET" request.

        :params tinfo: the info tuple of the test case.
        :return: whether the test is passed.
        """
        print(tinfo)
        path = self.replace_ids_in_path(tinfo[1])
        res = requests.get(self.baseurl + path)

        if res.status_code != tinfo[2]:
            print('Unexpected status code: %d' % (res.status_code))
            return False

        resj = res.json()
        if res.status_code == 200:
            # update ID tabs with real IDs
            for pat, key in self.get_cases:
                if re.match(pat, path):
                    for o, k in zip(resj, tinfo[4]):
                        self.ids[k] = o[key]
                    break

            # "date_and_time" check
            if re.match(r'orders/.+', path):
                if 'payment_processing' in resj and 'date_and_time' in resj['payment_processing']:
                    resj['payment_processing']['date_and_time'] = \
                        resj['payment_processing']['date_and_time'][:10]

            # compare the response body with expected response
            expected_res = self.replace_ids_in_res(self.f2o(tinfo[3]))
            if orderize(expected_res) != orderize(resj):
                print('Unexpected response:\n%s' % (resj))
                print('Expected:\n%s' % (expected_res))
                return False

        elif res.status_code == 400:
            return self.check_response_400(resj, path)

        return True


    def test_post(self, tinfo):
        """
        Test a "POST" request.

        :params tinfo: the info tuple of the test case.
        :return: whether the test is passed.
        """
        path = self.replace_ids_in_path(tinfo[1])
        data = self.replace_ids_in_req(self.f2o(tinfo[2]))
        res = requests.post(self.baseurl + path, json=data)

        if res.status_code != tinfo[3]:
            print('Unexpected status code: %d' % (res.status_code))
            return False

        resj = res.json()
        if res.status_code == 201:
            # update ID tabs with real IDs
            for pat, key in self.post_cases:
                if re.match(pat, path):
                    if key in resj:
                        self.ids[tinfo[5]] = resj[key]
                        return True
                    else:
                        print('Unexpected response:\n%s' % (resj))
                        return False
        elif res.status_code == 400:
            return self.check_response_400(resj, path)

        return False


    def test_put(self, tinfo):
        """
        Test a "PUT" request.

        :params tinfo: the info tuple of the test case.
        :return: whether the test is passed.
        """
        path = self.replace_ids_in_path(tinfo[1])
        data = self.replace_ids_in_req(self.f2o(tinfo[2]))
        res = requests.put(self.baseurl + path, json=data)

        if res.status_code != tinfo[3]:
            print('Unexpected status code: %d' % (res.status_code))
            return False

        if res.status_code == 400:
            return self.check_response_400(res.json(), path)

        return True


    def test_delete(self, tinfo):
        """
        Test a "DELETE" request.

        :params tinfo: the info tuple of the test case.
        :return: whether the test is passed.
        """
        path = self.replace_ids_in_path(tinfo[1])
        res = requests.delete(self.baseurl + path)

        if res.status_code != tinfo[2]:
            print('Unexpected status code: %d' % (res.status_code))
            return False

        return True


def main():
    ptc = ParkpayTestClient(BASE_URL, tests)
    ptc.run()

if __name__ == '__main__':
    main()
