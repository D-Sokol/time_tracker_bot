#!/usr/bin/env python3

from test import BaseApplicationTest
from .management import *

class TestUsers(BaseApplicationTest):
    def test_ensure(self):
        user = ensure_user(42)
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, 42)
