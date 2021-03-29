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


class SaveCouriersSimple(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = app
        app.config.from_object("app.main.config.TestingConfig")
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def get_stat_code_and_data(self, test_data):
        rv = self.client.post("/couriers/", data=json.dumps(test_data), content_type="application/json")
        return rv.status_code, json.loads(rv.get_data())

    def test_couriers_post(self):
        tests_count = 4
        for i in range(tests_count):
            test_data, ans_data = get_test_and_answer("couriers_post_simple", i)

            status_code, resp_data = self.get_stat_code_and_data(test_data)

            self.assertEqual(status_code, ans_data["code"])
            if ans_data["code"] not in [400, 404]:
                self.assertCountEqual(ans_data["ans"], resp_data)


if __name__ == "__main__":
    unittest.main()
