import uuid
from typing import Optional

from office365.onedrive.contenttypes.content_type import ContentType
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestContentType(GraphDelegatedTestCase):
    target_ct: Optional[ContentType] = None

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_get_compatible_hub_content_types(self):
        """Get compatible hub content types"""
        cts = self.client.sites.root.content_types.get_compatible_hub_content_types().execute_query()
        self.assertIsNotNone(cts.resource_path)

    @requires_delegated_permission_or_role("Sites.Manage.All", "Sites.FullControl.All", roles=["Global Administrator"])
    def test2_create_site_content_type(self):
        """Create a site content type"""
        name = "docSet" + uuid.uuid4().hex
        ct = self.client.sites.root.content_types.add(name, "0x0120D520").execute_query()
        assert ct.resource_path is not None
        TestContentType.target_ct = ct

    @requires_delegated_permission_or_role("Sites.FullControl.All", roles=["Global Administrator"])
    def test3_publish(self):
        """Publish a site content type"""
        assert TestContentType.target_ct is not None
        result = TestContentType.target_ct.publish().execute_query()
        self.assertFalse(result.resource_path)

    @requires_delegated_permission_or_role("Sites.FullControl.All", roles=["Global Administrator"])
    def test4_is_published(self):
        """Check if a site content type is published"""
        assert TestContentType.target_ct is not None
        result = TestContentType.target_ct.is_published().execute_query()
        self.assertTrue(result.value)

    def test5_list_site_content_types(self):
        """List all site content types"""
        result = self.client.sites.root.content_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role("Sites.FullControl.All", roles=["Global Administrator"])
    def test6_unpublish(self):
        """Unpublish a site content type"""
        assert TestContentType.target_ct is not None
        result = TestContentType.target_ct.unpublish().is_published().execute_query()
        self.assertFalse(result.value)

    @requires_delegated_permission_or_role("Sites.Manage.All", "Sites.FullControl.All", roles=["Global Administrator"])
    def test7_delete_site_content_type(self):
        """Delete a site content type"""
        ct_to_del = TestContentType.target_ct
        assert ct_to_del is not None
        ct_to_del.delete_object().execute_query()

    @requires_delegated_permission_or_role(
        "Sites.Read.All",
        "Sites.FullControl.All",
        "Sites.Manage.All",
        "Sites.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test8_get_applicable_content_types_for_list(self):
        """Get applicable content types for a list"""
        site = self.client.sites.root
        doc_lib = site.lists["Documents"]
        cts = site.get_applicable_content_types_for_list(doc_lib).execute_query()
        self.assertIsNotNone(cts.resource_path)
