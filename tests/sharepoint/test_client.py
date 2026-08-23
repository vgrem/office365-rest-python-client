"""Tests for SharePoint client context and query execution (connection, batching, query options)."""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.users.id_info import UserIdInfo
from office365.sharepoint.webs.web import Web

from tests import (
    create_unique_file_name,
    create_unique_name,
    test_cert_path,
    test_cert_thumbprint,
    test_client_id,
    test_password,
    test_site_url,
    test_team_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointClient(SPTestCase):
    """Tests for SharePoint client context connection and query execution."""

    def test_01_connect_with_client_certificate(self):
        """Connect using app principal credentials."""
        ctx = ClientContext(test_site_url).with_client_certificate(
            test_tenant, test_client_id, test_cert_thumbprint, test_cert_path
        )
        result = Web.get_context_web_information(ctx).execute_query()
        self.assertIsNotNone(result.value.WebFullUrl)

    def test_03_connect_with_user_credentials(self):
        """Connect using username and password credentials."""
        ctx = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        result = Web.get_context_web_information(ctx).execute_query()
        self.assertIsNotNone(result.value.WebFullUrl)

    def test_04_init_from_url(self):
        """Initialize client context from a page URL."""
        page_url = f"{test_team_site_url}/SitePages/Home.aspx"
        ctx = ClientContext.from_url(page_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        web = ctx.web.get().execute_query()
        self.assertIsNotNone(web.url)

    def test_05_execute_multiple_queries_sequentially(self):
        """Execute multiple queries sequentially."""
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        current_user = client.web.current_user
        client.load(current_user)
        current_web = client.web
        client.load(current_web)
        client.execute_query()
        self.assertIsNotNone(current_web.url)
        self.assertIsNotNone(current_user.user_id)

    def test_06_execute_get_batch_request(self):
        """Execute a GET batch request."""
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        current_user = client.web.current_user
        client.load(current_user)
        current_web = client.web
        client.load(current_web)
        client.execute_batch()
        self.assertIsNotNone(current_web.url)
        self.assertIsNotNone(current_user.user_id)
        self.assertIsInstance(current_user.user_id, UserIdInfo)

    def test_07_execute_update_batch_request(self):
        """Execute an UPDATE batch request."""
        web = self.client.web
        new_web_title = create_unique_name("Site")
        web.set_property("Title", new_web_title).update()
        self.client.execute_batch()

        updated_web = self.client.web.get().execute_query()
        self.assertEqual(updated_web.title, new_web_title)

    def test_08_execute_get_and_update_batch_request(self):
        """Execute combined GET and UPDATE batch requests."""
        page_url = "SitePages/Home.aspx"
        list_item = self.client.web.get_file_by_server_relative_url(page_url).listItemAllFields
        new_title = create_unique_name("Page")
        list_item.set_property("Title", new_title).update()
        self.client.execute_batch()

        updated_list_item = list_item.get().execute_query()
        self.assertEqual(updated_list_item.properties["Title"], new_title)

    def test_10_get_and_delete_batch_request(self):
        """Execute get and delete batch requests for a file."""
        file_name = create_unique_file_name("TestFile", "txt")
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        list_pages = client.web.lists.get_by_title("Documents")
        files = list_pages.root_folder.files.get().execute_query()
        files_count_before = len(files)
        new_file = list_pages.root_folder.upload_file(file_name, "-some content goes here-").execute_query()
        self.assertTrue(new_file.name, file_name)

        new_file.delete_object()
        files_after = list_pages.root_folder.files
        client.load(files_after)
        client.execute_batch()
        self.assertEqual(len(files_after), files_count_before)

    def test_13_ensure_property(self):
        """Ensure a property is loaded before accessing it."""
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        me = client.web.current_user.get()
        site = client.site

        def _owner_loaded():
            self.assertIsNotNone(site.owner.id)

        site.ensure_property("Owner").after_execute(lambda _: _owner_loaded())
        lib = client.web.default_document_library().get()
        client.execute_query()
        self.assertIsNotNone(me.login_name)
        self.assertIsNotNone(lib.title)
