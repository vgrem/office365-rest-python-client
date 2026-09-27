"""Content types — site-level and content type hub management.

Tests cover:
  - Getting compatible hub content types
  - Listing all site content types
  - Getting applicable content types for a list
  - Creating, publishing, unpublishing, and deleting a content type in the content type hub
"""

from __future__ import annotations

import unittest
import uuid
from typing import ClassVar, Optional

from office365.graph_client import GraphClient
from office365.onedrive.contenttypes.content_type import ContentType
from office365.onedrive.sites.site import Site
from office365.runtime.client_request_exception import ClientRequestException
from tests import test_content_type_hub_url, test_root_site_url
from tests.decorators import requires_application, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase


def _resolve_content_type_hub(client: GraphClient) -> Optional[Site]:
    """Resolve the tenant content type hub site.

    Prefers the configured hub URL, falling back to the SharePoint convention. Returns ``None`` when neither
    candidate is reachable.
    """
    candidates = [test_content_type_hub_url, f"{test_root_site_url}/sites/contentTypeHub"]
    for url in dict.fromkeys(u for u in candidates if u):
        try:
            return client.sites.get_by_url(url).get().execute_query()
        except ClientRequestException:
            continue
    return None


class TestContentType(GraphDelegatedTestCase):
    """Read-only site content type queries."""

    @requires_delegated(
        "Sites.Read.All",
        "Sites.Manage.All",
        "Sites.FullControl.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_get_compatible_hub_content_types(self):
        """Getting compatible hub content types returns a valid collection."""
        cts = self.client.sites.root.content_types.get_compatible_hub_content_types().execute_query()
        self.assertIsNotNone(cts.resource_path)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.Manage.All",
        "Sites.FullControl.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_list_site_content_types(self):
        """Listing all site content types returns a valid collection."""
        result = self.client.sites.root.content_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.FullControl.All",
        "Sites.Manage.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_get_applicable_content_types_for_list(self):
        """Getting applicable content types for the Documents list returns results."""
        site = self.client.sites.root
        doc_lib = site.lists["Documents"]
        cts = site.get_applicable_content_types_for_list(doc_lib).execute_query()
        self.assertIsNotNone(cts.resource_path)


class TestContentTypeHub(GraphApplicationTestCase):
    """Content type lifecycle in the tenant content type hub.

    Hub operations require application permissions because the content type hub site collection is typically not
    accessible to delegated users.
    """

    target_ct: ClassVar[Optional[ContentType]] = None
    hub: ClassVar[Optional[Site]] = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        hub = _resolve_content_type_hub(cls.client)
        if hub is None:
            raise unittest.SkipTest("Content type hub site is not accessible")
        cls.hub = hub

    @requires_application("Sites.FullControl.All")
    def test_01_create_site_content_type(self):
        """Creating a document set content type in the hub should succeed."""
        assert self.hub is not None
        name = "docSet" + uuid.uuid4().hex
        ct = self.hub.content_types.add(name, "0x0120D520").execute_query()
        self.assertIsNotNone(ct.resource_path)
        self.assertIsNotNone(ct.id)
        TestContentTypeHub.target_ct = ct

    @requires_application("Sites.FullControl.All")
    def test_02_publish_content_type(self):
        """Publishing a content type in the hub should succeed."""
        ct = TestContentTypeHub.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")
        ct.publish().execute_query()

    @requires_application("Sites.FullControl.All")
    def test_03_is_published(self):
        """After publishing, the is_published check should return True."""
        ct = TestContentTypeHub.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")
        result = ct.is_published().execute_query()
        self.assertTrue(result.value)

    @requires_application("Sites.FullControl.All")
    def test_04_unpublish_content_type(self):
        """Unpublishing a content type and verifying is_published returns False."""
        ct = TestContentTypeHub.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")
        ct.unpublish().execute_query()
        result = ct.is_published().execute_query()
        self.assertFalse(result.value)

    @requires_application("Sites.FullControl.All")
    def test_05_delete_site_content_type(self):
        """Deleting a content type from the hub should succeed."""
        ct = TestContentTypeHub.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")
        ct.delete_object().execute_query()
        TestContentTypeHub.target_ct = None

    @classmethod
    def tearDownClass(cls) -> None:
        ct = cls.target_ct
        if ct and ct.resource_path:
            try:
                ct.delete_object().execute_query()
            except Exception:
                pass
