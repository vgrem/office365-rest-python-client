import uuid

from office365.onedrive.internal.paths.url import UrlPath
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath
from tests import test_team_site_url
from tests.graph_case import GraphTestCase


class TestGraphClient(GraphTestCase):
    def test1_execute_batch_get_requests(self):
        current_user = (
            self.client.me.get()
        )  # 1.1: construct query to retrieve current user
        my_drive = (
            self.client.me.drive.get()
        )  # 1.2: construct query to retrieve my drive
        self.client.execute_batch()  # 2:submit query to the server
        self.assertIsNotNone(current_user.id)
        self.assertIsNotNone(my_drive.web_url)

    def test2_build_resource_path(self):
        result = self.client.me.drive.root.get().execute_query()
        self.assertEqual(
            "/me/drive/items/{0}".format(result.id), str(result.resource_path)
        )

    def test3_build_url_resource_path(self):
        path = UrlPath(
            "Sample.docx",
            ResourcePath("root", ResourcePath("drive", self.client.me.resource_path)),
        )
        self.assertEqual(str(path), "/me/drive/root:/Sample.docx:/")

    def test4_build_url_nested_resource_path(self):
        parent_path = ResourcePath(
            "root", ResourcePath("drive", self.client.me.resource_path)
        )
        path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent_path)))
        self.assertEqual("/me/drive/root:/archive/2018/Sample.docx:/", str(path))

    def test5_resolve_drive_url_path(self):
        parent_path = self.client.me.drive.root.resource_path
        path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent_path)))
        item_id = uuid.uuid4().hex
        path.patch(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test6_resolve_drive_children_path(self):
        path = self.client.me.drive.root.children.resource_path
        item_id = uuid.uuid4().hex
        path.patch(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test7_build_drive_children_path(self):
        item_id = uuid.uuid4().hex
        path = self.client.sites.root.drive.items[item_id].children.resource_path
        self.assertEqual(f"/sites/root/drive/items/{item_id}/children", str(path))

    def test9_resolve_site_url_path(self):
        site = self.client.sites.get_by_url(test_team_site_url).execute_query()
        self.assertEqual(
            f"{str(self.client.sites.resource_path)}/{site.id}", str(site.resource_path)
        )

    def test_10_resolve_drive_root_path(self):
        path = self.client.me.drive.root.resource_path
        item_id = uuid.uuid4().hex
        path.patch(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test_11_build_site_root_path(self):
        site = self.client.sites.root.get().execute_query()
        self.assertEqual(f"/sites/{site.id}", str(site.resource_path))

    def test_12_resolve_term_children_path(self):
        group_id = uuid.uuid4().hex
        set_id = uuid.uuid4().hex
        term_id = uuid.uuid4().hex
        path = (
            self.client.sites.root.term_store.groups[group_id]
            .sets[set_id]
            .children.resource_path
        )
        path = path.patch(term_id)
        self.assertEqual(
            f"/sites/root/termStore/groups/{group_id}/sets/{set_id}/terms/{term_id}",
            str(path),
        )

    def test_13_resolve_me_resource_path(self):
        current_user = self.client.me.get().execute_query()
        self.assertEqual(
            "/users/{0}".format(current_user.id), str(current_user.resource_path)
        )

    def test_15_resolve_my_drive_resource_path(self):
        my_drive = self.client.me.drive.get().execute_query()
        self.assertEqual("/drives/{0}".format(my_drive.id), str(my_drive.resource_path))

    def test_16_resolve_entity_type_name(self):
        name = self.client.me.joined_teams.entity_type_name
        self.assertEqual("Collection(microsoft.graph.team)", name)

    def test_17_build_path_from_url(self):
        path_str = "/teams('7f919b9f-c220-4290-a4d8-5ff9300d1296')/operations('dc97f61a-0040-436f-ac09-427cd2456fd8')"
        path = ODataPathBuilder.parse_url(path_str)
        self.assertIsNotNone(path.segment)
