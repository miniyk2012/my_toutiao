import unittest

from app import app
from ext import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.context.pop()
