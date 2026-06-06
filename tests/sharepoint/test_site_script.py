"""Tests for SharePoint site script creation, listing, and deletion via SiteScriptUtility."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.sitescripts.metadata import SiteScriptMetadata
from office365.sharepoint.sitescripts.utility import SiteScriptUtility

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSiteScript(SPTestCase):
    """Test SharePoint site script operations."""

    site_script_meta: ClassVar[Optional[SiteScriptMetadata]] = None
    site_script_count: ClassVar[Optional[int]] = None

    def test_01_create(self):
        """Create a new site script."""
        script = {
            "$schema": "schema.json",
            "actions": [{"verb": "applyTheme", "themeName": "Contoso Theme"}],
            "bindata": {},
            "version": 1,
        }

        result = SiteScriptUtility.create_site_script(self.client, "Contoso theme script", "", script).execute_query()
        self.assertIsNotNone(result.value)
        TestSiteScript.site_script_meta = result.value

    def test_02_list_site_scripts(self):
        """List existing site scripts."""
        result = SiteScriptUtility.get_site_scripts(self.client).execute_query()
        self.assertIsNotNone(result.value)
        TestSiteScript.site_script_count = len(result.value)

    def test_03_delete_site_script(self):
        """Delete the created site script."""
        site_script_meta = TestSiteScript.site_script_meta
        if not site_script_meta:
            self.skipTest("No site script metadata from previous test")
        site_script_id = site_script_meta.Id
        if not site_script_id:
            self.skipTest("No site script Id from previous test")
        site_script_count = TestSiteScript.site_script_count
        if site_script_count is None:
            self.skipTest("No site script count from previous test")
        SiteScriptUtility.delete_site_script(self.client, site_script_id).execute_query()
        result_after = SiteScriptUtility.get_site_scripts(self.client).execute_query()
        self.assertEqual(site_script_count - 1, len(result_after.value))
