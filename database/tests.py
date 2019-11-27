#!/usr/bin/env python3
from datetime import datetime, timedelta

from test import BaseApplicationTest
from .management import *
from .timezone import parse_time, get_timezone, convert_to_tz


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
        user = ensure_user(42)
        begin_interval(42)
        record1 = end_interval(42)
        begin_interval(42)
        record2 = end_interval(42)
        delete_record(record2.record_id)
        self.assertListEqual(user.records, [record1])
        self.assertEqual(Record.query.count(), 1)

    def test_duration(self):
        now = datetime.now()
        delta = timedelta(hours=1, minutes=12, seconds=4)
        for i in range(10):
            record = create_record(42, now + i * delta, now + (i+1) * delta)
            self.assertEqual(record.begin_time, now + i * delta)
            self.assertEqual(record.end_time, now + (i+1) * delta)
            self.assertEqual(record.duration(), '1:12:04')


class TestTimeZone(BaseApplicationTest):
    def assert_offset(self, tz, min_offset):
        dt = datetime.now()
        self.assertEqual(tz.utcoffset(dt).total_seconds(), 60 * min_offset)

    def test_parse_time(self):
        offsets = [0, 60, -60, 360, -360, 14, -14]
        responses = ['+00:00', '+01:00', '-01:00', '+06:00', '-06:00', '+00:14', '-00:14']
        assert len(offsets) == len(responses)

        for offset, response in zip(offsets, responses):
            self.assertEqual(response, parse_time(offset))

    def test_get_tz(self):
        with self.subTest('From timezone'):
            self.assert_offset(get_timezone('Asia/Hong_Kong'), 480)
        with self.subTest('From offset as string'):
            self.assert_offset(get_timezone('2:00'), 120)
            self.assert_offset(get_timezone('+2:00'), 120)
            self.assert_offset(get_timezone('-2:00'), -120)
        with self.subTest('From offset as number'):
            for i in range(-130, 131, 13):
                self.assert_offset(get_timezone(i), i)
        with self.subTest('From UTC'):
            self.assert_offset(get_timezone(), 0)
            self.assert_offset(get_timezone('UTC'), 0)

    def test_convert_to_tz(self):
        dt = datetime.now()
        for offset in range(-130, 131, 13):
            tz = get_timezone(offset)
            tz = convert_to_tz(dt, tz).tzinfo
            self.assert_offset(tz, offset)


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
        user1 = ensure_user(42)
        user2 = ensure_user(43)

        begin_interval(42)
        begin_interval(43)
        end_interval(43)
        begin_interval(43)
        end_interval(43)
        end_interval(42)

        self.assertEqual(len(user1.records), 1)
        self.assertEqual(len(user2.records), 2)

        delete_user(43)
        self.assertEqual(get_users_count(), 1)
        self.assertEqual(Record.query.count(), 1)

    def test_last_record(self):
        pass


class TestUsersWithTimezones(BaseApplicationTest):
    def test_set_tz(self):
        pass

    def test_get_tz(self):
        pass

    def test_user_wrap_time(self):
        pass

    def test_record_format_time(self):
        pass
