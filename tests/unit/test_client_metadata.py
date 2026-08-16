"""Offline unit tests for client metadata, query options and ClientResult (no credentials)."""

from __future__ import annotations

import unittest

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.odata.query_options_builder import QueryOptionsBuilder
from office365.runtime.odata.type import ODataType
from office365.runtime.types.collections import GuidCollection, StringCollection
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.secondary_administrators_fields_data import (
    SecondaryAdministratorsFieldsData,
)
from tests import test_site_url


class TestClientMetadata(unittest.TestCase):
    """Entity type-name resolution, query-option building and ClientResult wrapping."""

    def test_entity_type_name_resolution(self):
        guid_coll = GuidCollection()
        self.assertEqual(guid_coll.entity_type_name, "Collection(Edm.Guid)")

        custom_type_name = ODataType.resolve_type_name(SecondaryAdministratorsFieldsData)
        self.assertEqual(
            custom_type_name,
            "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData",
        )

        str_type_name = ODataType.resolve_type_name(StringCollection)
        self.assertEqual(str_type_name, "Collection(Edm.String)")

        str_col = StringCollection()
        self.assertEqual(str_col.entity_type_name, "Collection(Edm.String)")

        type_item = SecondaryAdministratorsFieldsData()
        self.assertEqual(
            type_item.entity_type_name,
            "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData",
        )

        type_col = ClientValueCollection(SecondaryAdministratorsFieldsData)
        expected_type = "Collection(Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData)"
        self.assertEqual(type_col.entity_type_name, expected_type)

    def test_build_query_options(self):
        client = ClientContext(test_site_url)
        lib = client.web.default_document_library()
        options = QueryOptionsBuilder.build(lib, ["Author", "Comments"])
        self.assertEqual(str(options), "$select=Author,Comments&$expand=Author")

    def test_client_result_wraps_collection(self):
        client = ClientContext(test_site_url)
        result = ClientResult(client, StringCollection())
        self.assertIsInstance(result.value, StringCollection)
