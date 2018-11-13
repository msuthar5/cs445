import unittest
import requests
import json
import datetime

class TestStringMethods(unittest.TestCase):

    def get_request(self, args):
        URL = args[1]
        resp = args[2]
        status_code = args[3]
        r = requests.get(URL)
        self.assertEqual(r.json(), resp)

    def post_request(self):
        pass
    def put_request(self):
        pass
    def delete_request(self):
        pass

    def setUp(self):
        file = open("test_data.json", "r+")
        content = file.read()
        file.close()
        self.data = json.loads(content)
        self.headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        self.maxDiff = None

    def test_tc00_payload(self):
        args = self.data["0"]
        URL = args[1]
        resp = args[2]
        status_code = args[3]
        r = requests.get(URL, headers = self.headers)
        self.assertEqual(r.json(), resp)


    def test_tc01_payload(self):
        args = self.data["1"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc02_payload(self):
        args = self.data["2"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc03_payload(self):
        args = self.data["3"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc04_payload(self):
        args = self.data["4"]

        r = requests.put(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.text, args[3])

    def test_tc05_payload(self):
        args = self.data["5"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc06_payload(self):
        args = self.data["6"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc07_payload(self):
        args = self.data["7"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc08_payload(self):
        args = self.data["8"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc09_payload(self):
        args = self.data["9"]

        r = requests.delete(args[1], headers=self.headers)
        self.assertEqual(r.text, args[2])

    def test_tc10_payload(self):
        args = self.data["10"]

        r = requests.delete(args[1], headers=self.headers)
        self.assertEqual(r.text, args[2])

    def test_tc11_payload(self):
        args = self.data["11"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc12_payload(self):
        args = self.data["12"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc13_payload(self):
        args = self.data["13"]

        args[2][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc14_payload(self):
        args = self.data["14"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc15_payload(self):
        args = self.data["15"]

        args[2]["orders"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc16_payload(self):
        args = self.data["16"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])


    def test_tc17_payload(self):
        args = self.data["17"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc18_payload(self):
        args = self.data["18"]

        args[2]["orders"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        args[2]["notes"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc19_payload(self):
        args = self.data["19"]

        args[2]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc20_payload(self):
        args = self.data["20"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc21_payload(self):
        args = self.data["21"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc22_payload(self):
        args = self.data["22"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc23_payload(self):
        args = self.data["23"]

        r = requests.post(args[2], data=json.dumps(args[1]), headers=self.headers)
        self.assertEqual(r.json(), args[3])

    def test_tc24_payload(self):
        args = self.data["24"]

        args[2][0]["notes"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        args[2][0]["notes"][1]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc25_payload(self):
        args = self.data["25"]

        #args[2][0]["notes"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        args[2]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc26_payload(self):
        args = self.data["26"]

        #args[2][0]["notes"][0]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        args[2]["payment_processing"]["date_and_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        args[2]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        args[2]["payment_processing"] = r.json()["payment_processing"]

        self.assertEqual(r.json(), args[2])

    def test_tc27_payload(self):
        args = self.data["27"]

        args[2][0]["date"] = args[2][1]["date"] = args[2][2]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])

    def test_tc28_payload(self):
        args = self.data["28"]

        args[2][0]["date"] = args[2][1]["date"] = datetime.date.today().strftime("%Y-%m-%d")
        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc29_payload(self):
        args = self.data["29"]

        r = requests.get(args[1], headers=self.headers)
        self.assertEqual(r.json(), args[2])

    def test_tc30_payload(self):
        args = self.data["30"]

        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])

    def test_tc31_payload(self):
        args = self.data["31"]

        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])

    def test_tc32_payload(self):
        args = self.data["32"]

        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])

    def test_tc33_payload(self):
        args = self.data["33"]

        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])


    def test_tc34_payload(self):
        args = self.data["34"]

        r = requests.get(args[1], headers=self.headers)

        self.assertEqual(r.json(), args[2])

if __name__ == '__main__':
    unittest.main()

