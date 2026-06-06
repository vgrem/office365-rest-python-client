"""Tests for SharePoint site design creation, listing, and deletion via SiteScriptUtility."""

from __future__ import annotations

from typing import ClassVar, Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from office365.sharepoint.sitescripts.utility import SiteScriptUtility

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSiteDesign(SPTestCase):
    """Test SharePoint site design operations."""

    site_design_metadata: ClassVar[Optional[SiteDesignMetadata]] = None
    site_design_count: ClassVar[Optional[int]] = None

    def test_01_create(self):
        """Create a new site design."""
        info = SiteDesignCreationInfo(
            Title="Contoso customer tracking",
            Description="Creates customer list and applies standard theme",
            SiteScriptIds=ClientValueCollection(UUID, [UUID("07702c07-0485-426f-b710-4704241caad9")]),
            WebTemplate="64",
        )
        result = SiteScriptUtility.create_site_design(self.client, info).execute_query()
        self.assertIsNotNone(result.value)
        TestSiteDesign.site_design_metadata = result.value

    def test_02_list(self):
        """List existing site designs."""
        result = SiteScriptUtility.get_site_designs(self.client).execute_query()
        self.assertIsNotNone(result.value)
        self.assertGreater(len(result.value), 0)
        TestSiteDesign.site_design_count = len(result.value)

    def test_03_delete(self):
        """Delete the created site design."""
        site_design_metadata = TestSiteDesign.site_design_metadata
        if not site_design_metadata:
            self.skipTest("No site design metadata from previous test")
        site_design_id = site_design_metadata.Id
        if not site_design_id:
            self.skipTest("No site design Id from previous test")
        site_design_count = TestSiteDesign.site_design_count
        if site_design_count is None:
            self.skipTest("No site design count from previous test")
        SiteScriptUtility.delete_site_design(self.client, site_design_id).execute_query()
        result = SiteScriptUtility.get_site_designs(self.client).execute_query()
        self.assertEqual(site_design_count - 1, len(result.value))
