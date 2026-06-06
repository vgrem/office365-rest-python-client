"""Tests for SharePoint sharing features including file sharing, unsharing, and sharing settings."""

from __future__ import annotations

from typing import ClassVar, Optional
from urllib.parse import urljoin

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.users.user import User
from office365.sharepoint.sharing.document_manager import DocumentSharingManager
from office365.sharepoint.sharing.object_sharing_information import (
    ObjectSharingInformation,
)
from office365.sharepoint.sharing.operation_status_code import (
    SharingOperationStatusCode,
)
from office365.sharepoint.sharing.result import SharingResult
from office365.sharepoint.sharing.role_type import RoleType
from office365.sharepoint.sharing.site_sharing_report_helper import (
    SiteSharingReportHelper,
)
from office365.sharepoint.webs.web import Web

from tests import (
    test_client_id,
    test_password,
    test_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointSharing(SPTestCase):
    """Test SharePoint sharing operations."""

    target_file_url = urljoin(test_site_url, "/SitePages/Home.aspx")
    target_user: ClassVar[Optional[User]] = None

    @classmethod
    def setUpClass(cls):
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        client.web.lists.ensure_site_pages_library().execute_query()
        current_user = client.web.current_user.get().execute_query()
        cls.target_user = current_user
        cls.client = client

    def test_01_get_role_def(self):
        """Get a role definition by role type."""
        role_def = DocumentSharingManager.get_role_definition(self.client, RoleType.Contributor).execute_query()
        self.assertTrue(role_def.name, "Full Control")

    def test_02_get_object_sharing_settings(self):
        """Get object sharing settings for a target file."""
        result = Web.get_object_sharing_settings(self.client, self.target_file_url, None, True).execute_query()
        self.assertIsNotNone(result.web_url)

    def test_03_get_file_sharing_info(self):
        """Get sharing information for a list item."""
        list_item = self.client.web.get_list_item("/SitePages/Home.aspx")
        sharing_info = list_item.get_sharing_information().execute_query()
        self.assertIsNotNone(list_item.resource_path)
        self.assertIsInstance(sharing_info, ObjectSharingInformation)

    def test_04_share_file(self):
        """Share a file with another user."""
        target_user = TestSharePointSharing.target_user
        if not target_user or not target_user.user_principal_name:
            self.skipTest("No target user principal name available")
        target_file_item = self.client.web.get_list_item("/SitePages/Home.aspx")
        result = target_file_item.share(target_user.user_principal_name).execute_query()
        self.assertIsNone(result.error_message)

    def test_05_get_shared_with_me_items(self):
        """Get items shared with the current user."""
        from office365.sharepoint.portal.userprofiles.sharedwithme.item_collection import (
            SharedWithMeItemCollection,
        )

        result = SharedWithMeItemCollection.get_shared_with_me_items(self.client, 10).execute_query()
        self.assertIsNotNone(result.value)

    def test_06_unshare_file(self):
        """Unshare a previously shared file."""
        target_file_item = self.client.web.get_list_item("/SitePages/Home.aspx")
        result = target_file_item.unshare().execute_query()
        self.assertIsInstance(result, SharingResult)
        self.assertIsNone(result.error_message)

    def test_07_share_web(self):
        """Share the web with another user."""
        target_user = TestSharePointSharing.target_user
        if not target_user:
            self.skipTest("No target user from setup")
        result = self.client.web.share(target_user.user_principal_name).execute_query()
        self.assertIsInstance(result, SharingResult)
        self.assertEqual(result.status_code, SharingOperationStatusCode.CompletedSuccessfully)
        self.assertIsNone(result.error_message)

    def test_08_unshare_web(self):
        """Unshare the web."""
        result = self.client.web.unshare().execute_query()
        self.assertIsInstance(result, SharingResult)

    def test_09_get_web_sharing_information(self):
        """Get web sharing information."""
        result = ObjectSharingInformation.get_web_sharing_information(self.client).execute_query()
        self.assertIsNotNone(result.properties)

    def test_10_get_site_sharing_report_capabilities(self):
        """Get site sharing report capabilities."""
        result = SiteSharingReportHelper.get_site_sharing_report_capabilities(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_11_get_list_sharing_settings(self):
        """Get sharing settings for the default document library."""
        result = self.client.web.default_document_library().get_sharing_settings().execute_query()
        self.assertIsNotNone(result.list_id)
