"""Offline unit tests for query-option URL serialization and delta tokens."""

from __future__ import annotations

import unittest

from office365.delta_collection import DeltaCollection
from office365.graph_client import GraphClient
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.queries.read_entity import ReadEntityQuery


class TestQueryOptionsUrl(unittest.TestCase):
    """QueryOptions.to_url must prefix $ only for standard OData options."""

    def test_standard_options_keep_dollar_prefix(self):
        q = QueryOptions()
        q.select = ["displayName"]
        q.filter = "startswith(displayName,'A')"
        q.top = 10
        self.assertEqual(
            q.to_url(),
            "$select=displayName&$filter=startswith(displayName,'A')&$top=10",
        )

    def test_custom_params_are_verbatim(self):
        q = QueryOptions()
        q.custom["token"] = "latest"
        q.custom["$search"] = "pizza"
        q.custom["$count"] = "true"
        q.custom["$changeType"] = "created"
        self.assertEqual(q.to_url(), "token=latest&$search=pizza&$count=true&$changeType=created")


class TestDeltaToken(unittest.TestCase):
    """Delta requests must use ?token=... and expose a resumable token value."""

    def test_delta_url_uses_token_without_dollar(self):
        delta = GraphClient().me.drive.root.delta.token("abc123")
        self.assertEqual(
            ReadEntityQuery(delta).url,
            "https://graph.microsoft.com/v1.0/me/drive/root/delta?token=abc123",
        )

    def test_delta_token_parses_parenthesized_value(self):
        col = DeltaCollection(GraphClient(), DriveItem)
        col.set_property(
            "@odata.deltaLink",
            "https://graph.microsoft.com/v1.0/me/drive/root/delta?(token='MzslMjM0')",
        )
        self.assertEqual(col.delta_token, "MzslMjM0")

    def test_delta_token_parses_query_value(self):
        col = DeltaCollection(GraphClient(), DriveItem)
        col.set_property(
            "@odata.deltaLink",
            "https://graph.microsoft.com/v1.0/me/drive/root/delta?token=2021-09-29T20%3A00%3A00Z",
        )
        self.assertEqual(col.delta_token, "2021-09-29T20%3A00%3A00Z")

    def test_delta_token_parses_dollar_deltatoken(self):
        col = DeltaCollection(GraphClient(), DriveItem)
        col.set_property("@odata.deltaLink", "https://graph.microsoft.com/v1.0/users/delta?$deltatoken=latest")
        self.assertEqual(col.delta_token, "latest")


if __name__ == "__main__":
    unittest.main()
