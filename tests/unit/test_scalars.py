"""Offline tests for the scalar value conversion primitives (converters/scalars)."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from enum import Enum

from office365.runtime.converters.scalars import parse_bool, parse_datetime, parse_enum


class _Level(Enum):
    Standard = "standard"
    Premium = "premium"


class TestScalarConverters(unittest.TestCase):
    def test_parse_bool(self):
        self.assertIs(parse_bool("True"), True)
        self.assertIs(parse_bool("false"), False)
        self.assertIs(parse_bool("1"), True)
        self.assertIs(parse_bool("no"), False)
        self.assertIs(parse_bool(True), True)
        self.assertEqual(parse_bool("nope"), "nope")

    def test_parse_enum(self):
        self.assertIs(parse_enum(_Level, "standard"), _Level.Standard)
        self.assertIs(parse_enum(_Level, _Level.Premium), _Level.Premium)
        self.assertIsNone(parse_enum(_Level, "nope"))

    def test_parse_datetime_iso(self):
        self.assertEqual(parse_datetime("2025-01-15T12:34:56Z"), datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(parse_datetime("2025-01-15T12:34:56"), datetime(2025, 1, 15, 12, 34, 56))

    def test_parse_datetime_numeric_offset(self):
        value = "2025-01-15T12:34:56+00:00"
        parsed = parse_datetime(value)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.timetuple()[:6], (2025, 1, 15, 12, 34, 56))
        self.assertIsNotNone(parsed.tzinfo)

    def test_parse_datetime_offset_with_microseconds(self):
        value = "2025-01-15T12:34:56.123456+00:00"
        parsed = parse_datetime(value)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.microsecond, 123456)

    def test_parse_datetime_round_trip(self):
        value = datetime(2025, 1, 15, 12, 34, 56, 123456, tzinfo=timezone.utc)
        self.assertEqual(parse_datetime(value.isoformat()), value)

    def test_parse_datetime_naive_round_trip(self):
        value = datetime(2025, 1, 15, 12, 34, 56)
        self.assertEqual(parse_datetime(value.isoformat()), value)


if __name__ == "__main__":
    unittest.main()
