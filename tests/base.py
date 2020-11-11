import os
import unittest

os.environ["env"] = "test"

from app import app
from ext import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()
        print('-' * 50)
        print('\n' * 5)

    def tearDown(self):
        print('\n' * 5)
        print('-' * 50)
        self.context.pop()
        with app.app_context():
            db.drop_all()
