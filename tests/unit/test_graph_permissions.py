"""Offline tests for GraphClient permission guards."""

from __future__ import annotations

import unittest
from unittest import mock

from office365.graph_client import GraphClient


class _Result:
    def __init__(self, value):
        self.value = value

    def execute_query(self):
        return self

    def __iter__(self):
        return iter(self.value)


def _make_sku(part_number):
    sku = mock.Mock()
    sku.sku_part_number = part_number
    return sku


class TestRequireLicense(unittest.TestCase):
    def _make_client(self) -> GraphClient:
        return GraphClient(tenant="contoso.onmicrosoft.com")

    def test_passes_when_sku_matches(self):
        client = self._make_client()
        collection = mock.Mock()
        collection.get.return_value = _Result([_make_sku("BACKUP_STORAGE_ADDON"), _make_sku("ENTERPRISEPACK")])
        with mock.patch.object(GraphClient, "subscribed_skus", new_callable=mock.PropertyMock, return_value=collection):
            self.assertIs(client.require_license("BACKUP"), client)

    def test_exits_when_no_sku_matches(self):
        client = self._make_client()
        collection = mock.Mock()
        collection.get.return_value = _Result([_make_sku("ENTERPRISEPACK")])
        with mock.patch.object(GraphClient, "subscribed_skus", new_callable=mock.PropertyMock, return_value=collection):
            with self.assertRaises(SystemExit):
                client.require_license("BACKUP")

    def test_noop_without_keywords(self):
        client = self._make_client()
        self.assertIs(client.require_license(), client)


class TestRequireDelegatedPermission(unittest.TestCase):
    def _make_client(self) -> GraphClient:
        ctx = GraphClient(tenant="contoso.onmicrosoft.com")
        ctx.pending_request().authentication_context._client_id = "app-id"
        return ctx

    def test_passes_when_scope_granted(self):
        client = self._make_client()
        client.get_delegated_permissions = mock.Mock(  # type: ignore[method-assign]
            return_value=_Result(["User.Read", "Mail.Read"])
        )
        self.assertIs(client.require_delegated_permission("User.Read"), client)

    def test_exits_when_scope_missing(self):
        client = self._make_client()
        client.get_delegated_permissions = mock.Mock(  # type: ignore[method-assign]
            return_value=_Result(["Mail.Read"])
        )
        with self.assertRaises(SystemExit):
            client.require_delegated_permission("User.Read")

    def test_noop_without_scopes(self):
        client = self._make_client()
        self.assertIs(client.require_delegated_permission(), client)


if __name__ == "__main__":
    unittest.main()
