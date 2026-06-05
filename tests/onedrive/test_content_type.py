"""Content types — site-level and list-level content type management.

Tests cover:
  - Getting compatible hub content types
  - Creating a site content type with a base type
  - Publishing a site content type
  - Checking if a content type is published
  - Listing all site content types
  - Unpublishing a site content type
  - Getting applicable content types for a list
  - Deleting a site content type
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.onedrive.contenttypes.content_type import ContentType

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestContentType(GraphDelegatedTestCase):
    """Site content type CRUD, publish, unpublish, and list interactions."""

    target_ct: ClassVar[Optional[ContentType]] = None

    @requires_delegated(
        "Sites.Read.All", "Sites.Manage.All", "Sites.FullControl.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_get_compatible_hub_content_types(self):
        """Getting compatible hub content types returns a valid collection."""
        cts = self.client.sites.root.content_types.get_compatible_hub_content_types().execute_query()
        self.assertIsNotNone(cts.resource_path)

    @requires_delegated(
        "Sites.Manage.All", "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_create_site_content_type(self):
        """Creating a document set content type should succeed."""
        name = "docSet" + uuid.uuid4().hex
        ct = self.client.sites.root.content_types.add(name, "0x0120D520").execute_query()
        self.assertIsNotNone(ct.resource_path)
        self.assertIsNotNone(ct.get_property("id"))
        TestContentType.target_ct = ct

    @requires_delegated(
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_publish_content_type(self):
        """Publishing a site content type should succeed."""
        ct = TestContentType.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")

        ct.publish().execute_query()

    @requires_delegated(
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_04_is_published(self):
        """After publishing, the is_published check should return True."""
        ct = TestContentType.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")

        result = ct.is_published().execute_query()
        self.assertTrue(result.value)

    @requires_delegated(
        "Sites.Read.All", "Sites.Manage.All", "Sites.FullControl.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_05_list_site_content_types(self):
        """Listing all site content types returns a valid collection."""
        result = self.client.sites.root.content_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_06_unpublish_content_type(self):
        """Unpublishing a content type and verifying is_published returns False."""
        ct = TestContentType.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")

        ct.unpublish().execute_query()
        result = ct.is_published().execute_query()
        self.assertFalse(result.value)

    @requires_delegated(
        "Sites.Manage.All", "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_07_delete_site_content_type(self):
        """Deleting a site content type should succeed."""
        ct = TestContentType.target_ct
        if not ct:
            self.skipTest("No content type created from previous test")

        ct.delete_object().execute_query()
        TestContentType.target_ct = None

    @requires_delegated(
        "Sites.Read.All", "Sites.FullControl.All", "Sites.Manage.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_08_get_applicable_content_types_for_list(self):
        """Getting applicable content types for the Documents list returns results."""
        site = self.client.sites.root
        doc_lib = site.lists["Documents"]
        cts = site.get_applicable_content_types_for_list(doc_lib).execute_query()
        self.assertIsNotNone(cts.resource_path)

    @classmethod
    def tearDownClass(cls):
        ct = cls.target_ct
        if ct and ct.resource_path:
            try:
                ct.delete_object().execute_query()
            except Exception:
                pass
