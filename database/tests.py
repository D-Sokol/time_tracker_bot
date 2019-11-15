#!/usr/bin/env python3
from datetime import datetime

from test import BaseApplicationTest
from .management import *

class TestUsers(BaseApplicationTest):
    def test_ensure(self):
        user = ensure_user(42)
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id, 42)

        user2 = ensure_user(50)
        self.assertIsNotNone(user2)
        self.assertEqual(user2.user_id, 50)

        user1 = ensure_user(42)
        self.assertIsNotNone(user1)
        self.assertEqual(user, user1)
        self.assertNotEqual(user1, user2)

    def test_count(self):
        self.assertEqual(get_users_count(), 0)
        ensure_user(42)
        self.assertEqual(get_users_count(), 1)
        ensure_user(43)
        ensure_user(44)
        self.assertEqual(get_users_count(), 3)
        ensure_user(42)
        self.assertEqual(get_users_count(), 3)

    def test_delete(self):
        ensure_user(42)
        ensure_user(43)
        ensure_user(44)
        self.assertEqual(get_users_count(), 3)

        delete_user(44)
        self.assertEqual(get_users_count(), 2)

        ensure_user(44)
        self.assertEqual(get_users_count(), 3)

        # Should not raise exception.
        self.assertIsNone(delete_user(50))


class TestRecords(BaseApplicationTest):
    def test_create(self):
        ensure_user(42)
        record = create_record(42, datetime.now(), datetime.now())
        self.assertIsNotNone(record)
        self.assertIsInstance(record, Record)
        self.assertEqual(record.record_id, 1)
        self.assertEqual(record.user_id, 42)

    def test_delete(self):
        pass

    def test_duration(self):
        pass


class TestTimeZone(BaseApplicationTest):
    def test_parse_time(self):
        pass

    def test_get_tz(self):
        with self.subTest('From timezone'):
            pass
        with self.subTest('From offset as string'):
            pass
        with self.subTest('From offset as number'):
            pass
        with self.subTest('From UTC'):
            pass

    def test_convert_to_tz(self):
        pass

class TestUsersWithRecords(BaseApplicationTest):
    def test_creation_by_user(self):
        user = ensure_user(42)
        self.assertRaises(ValueError, end_interval, 42)
        self.assertIsNone(user.current_start_time)
        self.assertListEqual(user.records, [])

        self.assertIsInstance(begin_interval(42), str)
        self.assertIsNotNone(user.current_start_time)

        cancel_interval(42)
        self.assertIsNone(user.current_start_time)
        self.assertListEqual(user.records, [])

        begin_interval(42)
        end_interval(42)
        self.assertIsNone(user.current_start_time)
        self.assertRaises(ValueError, end_interval, 42)

        record = Record.query.first()
        self.assertIsNotNone(record)
        self.assertListEqual(user.records, [record])

    def test_cascade_deletion(self):
        pass

    def test_last_record(self):
        pass

    def test_user_wrap_time(self):
        pass

    def test_record_format_time(self):
        pass


class TestUsersWithTimezones(BaseApplicationTest):
    def test_set_tz(self):
        pass

    def test_get_tz(self):
        pass
