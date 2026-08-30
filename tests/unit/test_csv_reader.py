"""Offline tests for the collection import pipeline (csv_reader / from_csv / from_json)."""

from __future__ import annotations

import io
import unittest
import warnings
from datetime import datetime, timezone
from typing import cast

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.csv_reader import clean_records, coerce_records, read_csv_records
from office365.runtime.converters.csv_writer import write_csv
from tests.settings import cert_path, cert_thumbprint, client_id, tenant

CSV_TEXT = (
    "userPrincipalName,givenName,displayName,accountEnabled,officeLocation,"
    "passwordProfile/password,passwordProfile/forceChangePasswordNextSignIn,businessPhones\n"
    "jdoe@contoso.com,John,John Doe,True,Seattle,S3cret!,True,+1-555-0101; +1-555-0102\n"
)


def _graph_client() -> GraphClient:
    with open(cert_path, "r", encoding="utf-8") as f:
        private_key = f.read()
    return GraphClient(tenant=tenant).with_certificate(client_id, cert_thumbprint, private_key)


class TestCsvRecords(unittest.TestCase):
    def test_read_csv_records(self):
        records = read_csv_records(io.StringIO(CSV_TEXT))
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["userPrincipalName"], "jdoe@contoso.com")
        self.assertEqual(record["passwordProfile/password"], "S3cret!")

    def test_coerce_records(self):
        records = coerce_records(
            User,
            read_csv_records(io.StringIO(CSV_TEXT)),
        )
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["userPrincipalName"], "jdoe@contoso.com")
        self.assertEqual(record["passwordProfile"], {"password": "S3cret!", "forceChangePasswordNextSignIn": "True"})
        self.assertEqual(record["businessPhones"], ["+1-555-0101", "+1-555-0102"])

    def test_coerce_records_strips_non_importable_and_unknown(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            records = coerce_records(
                User,
                [
                    {
                        "userPrincipalName": "jdoe@contoso.com",
                        "id": "42",
                        "@odata.type": "user",
                        "noSuchColumn": "x",
                    }
                ],
            )
        self.assertEqual(records, [{"userPrincipalName": "jdoe@contoso.com"}])
        self.assertTrue(any("noSuchColumn" in str(w.message) for w in caught))

    def test_clean_records(self):
        records = clean_records(
            [
                {"userPrincipalName": "a@x.com", "id": "42", "@odata.type": "user", "givenName": None},
                {"userPrincipalName": "b@x.com"},
            ]
        )
        self.assertEqual(records, [{"userPrincipalName": "a@x.com"}, {"userPrincipalName": "b@x.com"}])


class TestImportPipeline(unittest.TestCase):
    def test_from_csv_queues_creates(self):
        client = _graph_client()
        users = client.users.from_csv(io.StringIO(CSV_TEXT))
        self.assertEqual(len(users), 1)
        self.assertEqual(len(client._queries), 1)
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("passwordProfile").password, "S3cret!")
        self.assertIs(user.get_property("passwordProfile").forceChangePasswordNextSignIn, True)
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])

    def test_from_json_queues_creates(self):
        client = _graph_client()
        users = client.users.from_json(
            [
                {
                    "userPrincipalName": "jdoe@contoso.com",
                    "displayName": "John Doe",
                    "accountEnabled": True,
                    "id": "42",
                    "@odata.type": "user",
                }
            ]
        )
        self.assertEqual(len(users), 1)
        self.assertEqual(len(client._queries), 1)
        self.assertIs(users[0].get_property("accountEnabled"), True)
        self.assertNotIn("id", users[0].properties)

    def test_round_trip_write_then_read(self):
        col = ClientObjectCollection(cast(ClientRuntimeContext, None), User, None)
        item = col.create_typed_object(
            {
                "userPrincipalName": "jdoe@contoso.com",
                "displayName": "John Doe",
                "accountEnabled": True,
                "createdDateTime": datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc),
                "businessPhones": ["+1-555-0101", "+1-555-0102"],
            }
        )
        col.add_child(item)
        col.query_options.select = [
            "userPrincipalName",
            "displayName",
            "accountEnabled",
            "createdDateTime",
            "businessPhones",
        ]
        out = io.StringIO()
        write_csv(col, out)

        client = _graph_client()
        users = client.users.from_csv(io.StringIO(out.getvalue()))
        user = users[0]
        self.assertIs(user.get_property("accountEnabled"), True)
        self.assertEqual(user.get_property("createdDateTime"), datetime(2025, 1, 15, 12, 34, 56, tzinfo=timezone.utc))
        self.assertEqual(list(user.get_property("businessPhones")), ["+1-555-0101", "+1-555-0102"])


if __name__ == "__main__":
    unittest.main()
