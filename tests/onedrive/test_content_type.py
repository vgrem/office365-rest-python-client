import uuid
from unittest import TestCase

from office365.graph_client import GraphClient
from office365.onedrive.contenttypes.content_type import ContentType
from tests import test_client_id, test_password, test_tenant, test_username
from tests.decorators import requires_delegated_permission


class TestContentType(TestCase):
    target_ct: ContentType = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = GraphClient(tenant=test_tenant).with_username_and_password(
            test_client_id, test_username, test_password
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_get_compatible_hub_content_types(self):
        cts = (
            self.client.sites.root.content_types.get_compatible_hub_content_types().execute_query()
        )
        self.assertIsNotNone(cts.resource_path)

    @requires_delegated_permission("Sites.Manage.All", "Sites.FullControl.All")
    def test2_create_site_content_type(self):
        name = "docSet" + uuid.uuid4().hex
        ct = self.client.sites.root.content_types.add(
            name, "0x0120D520"
        ).execute_query()
        self.assertIsNotNone(ct.resource_path)
        self.__class__.target_ct = ct

    @requires_delegated_permission("Sites.FullControl.All")
    def test3_publish(self):
        result = self.__class__.target_ct.publish().execute_query()
        self.assertFalse(result.resource_path)

    @requires_delegated_permission("Sites.FullControl.All")
    def test4_is_published(self):
        result = self.__class__.target_ct.is_published().execute_query()
        self.assertTrue(result.value)

    def test5_list_site_content_types(self):
        result = self.client.sites.root.content_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.FullControl.All")
    def test6_unpublish(self):
        result = self.__class__.target_ct.unpublish().is_published().execute_query()
        self.assertFalse(result.value)

    @requires_delegated_permission("Sites.Manage.All", "Sites.FullControl.All")
    def test7_delete_site_content_type(self):
        ct_to_del = self.__class__.target_ct
        ct_to_del.delete_object().execute_query()

    @requires_delegated_permission(
        "Sites.Read.All",
        "Sites.FullControl.All",
        "Sites.Manage.All",
        "Sites.ReadWrite.All",
    )
    def test8_get_applicable_content_types_for_list(self):
        site = self.client.sites.root
        doc_lib = site.lists["Documents"]
        cts = site.get_applicable_content_types_for_list(doc_lib).execute_query()
        self.assertIsNotNone(cts.resource_path)
