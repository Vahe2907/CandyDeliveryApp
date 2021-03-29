import json
import unittest
import os

from manage import app
from app.main import db

tests_data = os.path.join(os.getcwd(), "app", "test", "data")


def get_test_and_answer(subdir, test_id):
    test_path = os.path.join(tests_data, subdir, f"test{test_id}", "t.json")
    test_data = json.load(open(test_path, "r"))

    ans_path = os.path.join(tests_data, subdir, f"test{test_id}", "a.json")
    ans_data = json.load(open(ans_path, "r"))

    return test_data, ans_data


class CouriersIdPatch(unittest.TestCase):
    app = None

    def setUp(self):
        self.app = app
        app.config.from_object("app.main.config.TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_stat_code_and_data(self, courier_id, test_data):
        rv = self.client.patch(f"/couriers/{courier_id}", data=json.dumps(test_data), content_type="application/json")
        return rv.status_code, json.loads(rv.get_data())

    def get_stat_code_and_data_ext(self, route, tp, test_data):
        if tp == "patch":
            rv = self.client.patch(route, data=json.dumps(test_data), content_type="application/json")
        else:
            rv = self.client.post(route, data=json.dumps(test_data), content_type="application/json")

        return rv.status_code, json.loads(rv.get_data())

    def load_base_from(self, path):
        couriers_path = os.path.join(tests_data, path, "couriers.json")
        couriers_data = json.load(open(couriers_path, "r"))

        orders_path = os.path.join(tests_data, path, "orders.json")
        orders_data = json.load(open(orders_path, "r"))

        rv = self.client.post("/couriers/", data=json.dumps(couriers_data), content_type="application/json")
        self.assertEqual(rv.status_code, 201)

        rv = self.client.post("/orders/", data=json.dumps(orders_data), content_type="application/json")
        self.assertEqual(rv.status_code, 201)

    def test_couriers_id_patch(self):
        self.load_base_from("base_sample0")

        test_count = 2
        for i in range(test_count):
            test_data, ans_data = get_test_and_answer("couriers_id_patch_simple", i)

            status_code, resp_data = self.get_stat_code_and_data(test_data['id'], test_data['data'])

            if ans_data["code"] not in [400, 404]:
                self.assertCountEqual(ans_data["ans"], resp_data)
            self.assertEqual(status_code, ans_data["code"])

    def test_couriers_id_patch_and_assign(self):
        self.load_base_from("base_sample1")

        test_count = 2
        for i in range(test_count):
            test_data, ans_data = get_test_and_answer("couriers_id_patch_assign_simple", i)

            status_code, resp_data = None, None
            for command in test_data["commands"]:
                status_code, resp_data = self.get_stat_code_and_data_ext(command["route"],
                                                                         command["type"], command["data"])

            self.assertEqual(status_code, ans_data["code"])
            if ans_data["code"] not in [400, 404]:
                self.assertListEqual(ans_data["ans"]["orders"], resp_data["orders"])
                if ans_data["assign"]:
                    self.assertIn("assign_time", resp_data)
                else:
                    self.assertNotIn("assign_time", resp_data)


if __name__ == "__main__":
    unittest.main()
