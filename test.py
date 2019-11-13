#!/usr/bin/env python3

import unittest

from config import TestConfig
from server import create_server
from database import db

from database.tests import *

class BaseApplicationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_server(TestConfig)
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()


if __name__ == '__main__':
    unittest.main()
