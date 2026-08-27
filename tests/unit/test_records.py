"""Offline tests for the shared record projection (records.iter_records)."""

from __future__ import annotations

import io
import unittest
from datetime import datetime, timezone
from typing import cast

from office365.directory.users.user import User
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.csv_writer import write_csv
from office365.runtime.converters.records import iter_records


def _collection(properties: list[dict]) -> ClientObjectCollection:
    col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
    for props in properties:
        col.add_child(col.create_typed_object(props))
    return col


class TestIterRecords(unittest.TestCase):
    def test_plain_select(self):
        col = _collection(
            [
                {"userPrincipalName": "jdoe@contoso.com", "displayName": "John Doe", "accountEnabled": True},
                {"userPrincipalName": "asmith@contoso.com", "displayName": "Alice Smith", "accountEnabled": False},
            ]
        )
        col.query_options.select = ["displayName", "userPrincipalName"]
        self.assertEqual(
            iter_records(col),
            [
                {"displayName": "John Doe", "userPrincipalName": "jdoe@contoso.com"},
                {"displayName": "Alice Smith", "userPrincipalName": "asmith@contoso.com"},
            ],
        )

    def test_native_values_kept(self):
        col = _collection(
            [
                {
                    "displayName": "John",
                    "accountEnabled": True,
                    "createdDateTime": datetime(2025, 1, 15, tzinfo=timezone.utc),
                }
            ]
        )
        col.query_options.select = ["displayName", "accountEnabled", "createdDateTime"]
        record = iter_records(col)[0]
        self.assertIs(record["accountEnabled"], True)
        self.assertEqual(record["createdDateTime"], "2025-01-15T00:00:00+00:00")

    def test_no_select_all_props_sorted(self):
        col = _collection([{"b": 2, "a": 1}])
        self.assertEqual(list(iter_records(col)[0].keys()), ["a", "b"])

    def test_selected_but_missing_key_is_none_filled(self):
        col = _collection([{"displayName": "John"}])
        col.query_options.select = ["displayName", "mail"]
        self.assertEqual(iter_records(col), [{"displayName": "John", "mail": None}])

    def test_multiple_navs_raises(self):
        col = _collection([{"displayName": "John"}])
        col.query_options.select = ["members/displayName", "manager/displayName"]
        with self.assertRaises(ValueError):
            iter_records(col)

    def test_empty_collection(self):
        self.assertEqual(iter_records(_collection([])), [])

    def test_csv_parity(self):
        col = _collection(
            [
                {"displayName": "John", "accountEnabled": True, "businessPhones": ["+1-555-0101", "+1-555-0102"]},
            ]
        )
        col.query_options.select = ["displayName", "accountEnabled", "businessPhones"]
        out = io.StringIO()
        write_csv(col, out)
        self.assertEqual(
            out.getvalue(),
            "displayName,accountEnabled,businessPhones\r\nJohn,True,+1-555-0101; +1-555-0102\r\n",
        )


if __name__ == "__main__":
    unittest.main()
