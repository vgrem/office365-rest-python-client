"""Tests for SharePoint client context and query execution (connection, batching, query options)."""

from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.odata.query_options_builder import QueryOptionsBuilder
from office365.runtime.odata.type import ODataType
from office365.runtime.types.collections import GuidCollection, StringCollection
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.principal.users.id_info import UserIdInfo
from office365.sharepoint.tenant.administration.secondary_administrators_fields_data import (
    SecondaryAdministratorsFieldsData,
)
from office365.sharepoint.webs.web import Web

from tests import (
    create_unique_file_name,
    create_unique_name,
    test_client_credentials,
    test_client_id,
    test_client_secret,
    test_password,
    test_site_url,
    test_team_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointClient(SPTestCase):
    """Tests for SharePoint client context connection and query execution."""

    def test_01_connect_with_app_principal(self):
        """Connect using app principal credentials."""
        ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
        result = Web.get_context_web_information(ctx).execute_query()
        self.assertIsNotNone(result.value.WebFullUrl)

    def test_02_connect_with_app_principal_alt(self):
        """Connect using client ID and secret directly."""
        ctx = ClientContext(test_site_url).with_client_credentials(test_client_id, test_client_secret)
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
        client = ClientContext(test_site_url).with_credentials(test_client_credentials)
        web = client.web
        new_web_title = create_unique_name("Site")
        web.set_property("Title", new_web_title).update()
        client.execute_batch()

        updated_web = client.web.get().execute_query()
        self.assertEqual(updated_web.properties["Title"], new_web_title)

    def test_08_execute_get_and_update_batch_request(self):
        """Execute combined GET and UPDATE batch requests."""
        page_url = "/SitePages/Home.aspx"
        client = ClientContext(test_site_url).with_credentials(test_client_credentials)
        list_item = client.web.get_file_by_server_relative_url(page_url).listItemAllFields
        new_title = create_unique_name("Page")
        list_item.set_property("Title", new_title).update()
        client.execute_batch()

        updated_list_item = client.web.get_file_by_server_relative_url(page_url).listItemAllFields.get().execute_query()
        self.assertEqual(updated_list_item.properties["Title"], new_title)

    def test_09_create_and_delete_batch_request(self):
        """Placeholder for create and delete batch request test."""

    def test_10_get_and_delete_batch_request(self):
        """Execute get and delete batch requests for a file."""
        file_name = create_unique_file_name("TestFile", "txt")
        client = ClientContext(test_site_url).with_credentials(test_client_credentials)
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

    def test_11_get_entity_type_name(self):
        """Verify entity type name resolution for various types."""
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

    def test_12_build_query_options(self):
        """Build query options with select and expand."""
        client = ClientContext(test_site_url)
        lib = client.web.default_document_library()
        options = QueryOptionsBuilder.build(lib, ["Author", "Comments"])
        self.assertEqual(str(options), "$select=Author,Comments&$expand=Author")

    def test_13_ensure_property(self):
        """Ensure a property is loaded before accessing it."""
        client = ClientContext(test_site_url).with_credentials(test_client_credentials)
        me = client.web.current_user.get()
        site = client.site

        def _owner_loaded():
            self.assertIsNotNone(site.owner.id)

        site.ensure_property("Owner").after_execute(lambda _: _owner_loaded())
        lib = client.web.default_document_library().get()
        client.execute_query()
        self.assertIsNotNone(me.login_name)
        self.assertIsNotNone(lib.title)

    def test_14_test_client_result(self):
        """Verify ClientResult wrapping of a value collection."""
        client = ClientContext(test_site_url)
        result = ClientResult(client, StringCollection())
        self.assertIsInstance(result.value, StringCollection)

    def test_15_query_options_is_empty(self):
        """Verify that default QueryOptions is empty."""
        options = QueryOptions()
        self.assertTrue(options.is_empty)
