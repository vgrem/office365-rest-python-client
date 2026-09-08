"""Offline unit tests for polymorphic ``@odata.type`` handling (refs issue #921)."""

from __future__ import annotations

import unittest

from office365.directory.applications.application import Application
from office365.directory.groups.group import Group
from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.objects.object import DirectoryObject
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from office365.directory.users.user import User
from office365.intune.devices.device import Device
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.sharepoint.client_context import ClientContext
from tests import test_site_url


def _graph_request() -> ODataRequest:
    return ODataRequest("", V4JsonFormat())


class TestODataResponseType(unittest.TestCase):
    """Members are cast to concrete classes from ``@odata.type`` (exposed via ``entity_type_name``)."""

    def test_members_are_cast_to_concrete_types(self):
        ctx = ClientContext(test_site_url)
        payload = {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#directoryObjects",
            "value": [
                {"@odata.type": "#microsoft.graph.user", "id": "u1", "displayName": "Alice"},
                {"@odata.type": "#microsoft.graph.group", "id": "g1"},
                {"@odata.type": "#microsoft.graph.device", "id": "d1"},
                {"@odata.type": "#microsoft.graph.application", "id": "a1"},
                {"@odata.type": "#microsoft.graph.servicePrincipal", "id": "sp1"},
            ],
        }
        col = DirectoryObjectCollection(ctx)
        _graph_request().map_json(payload, col, V4JsonFormat())

        self.assertEqual(len(col), 5)  # noqa: PLR2004
        self.assertIsInstance(col[0], User)
        self.assertIsInstance(col[1], Group)
        self.assertIsInstance(col[2], Device)
        self.assertIsInstance(col[3], Application)
        self.assertIsInstance(col[4], ServicePrincipal)
        self.assertEqual(col[0].entity_type_name, "microsoft.graph.User")
        self.assertEqual(col[0].get_property("displayName"), "Alice")
        for item in col:
            self.assertNotIn("@odata.type", item.properties)
            self.assertNotIn("__odata_type", item.properties)

    def test_unknown_member_type_falls_back_to_directory_object(self):
        ctx = ClientContext(test_site_url)
        payload = {"value": [{"@odata.type": "#microsoft.graph.administrativeUnit", "id": "au1"}]}
        col = DirectoryObjectCollection(ctx)
        _graph_request().map_json(payload, col, V4JsonFormat())

        self.assertEqual(len(col), 1)
        self.assertIsInstance(col[0], DirectoryObject)
        self.assertNotIn("__odata_type", col[0].properties)

    def test_single_entity_keeps_class_type(self):
        ctx = ClientContext(test_site_url)
        payload = {"@odata.type": "#microsoft.graph.user", "id": "u1", "displayName": "Alice"}
        user = User(ctx)
        _graph_request().map_json(payload, user, V4JsonFormat())

        self.assertEqual(user.entity_type_name, "microsoft.graph.User")
        self.assertEqual(user.get_property("id"), "u1")
        self.assertNotIn("@odata.type", user.properties)
        self.assertNotIn("__odata_type", user.properties)

    def test_sharepoint_json_light_metadata_is_untouched(self):
        """JsonLight/SharePoint metadata must not leak into properties or type name."""
        ctx = ClientContext(test_site_url)
        payload = {"d": {"__metadata": {"type": "SP.Web"}, "Id": "web-1", "Url": "https://x"}}
        web = ctx.web
        ODataRequest(test_site_url, JsonLightFormat()).map_json(payload, web, JsonLightFormat())

        self.assertEqual(web.entity_type_name, "SP.Web")
        self.assertNotIn("__metadata", web.properties)


if __name__ == "__main__":
    unittest.main()
