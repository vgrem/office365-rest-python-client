from __future__ import annotations

import uuid

from tests import test_team_site_url
from tests.graph_case import GraphDelegatedTestCase


class TestGraphClient(GraphDelegatedTestCase):
    def test1_execute_batch_get_requests(self):
        current_user = self.client.me.get()  # 1.1: construct query to retrieve current user
        my_drive = self.client.me.drive.get()  # 1.2: construct query to retrieve my drive
        self.client.execute_batch()  # 2:submit query to the server
        self.assertIsNotNone(current_user.id)
        self.assertIsNotNone(my_drive.web_url)

    def test2_build_resource_path(self):
        result = self.client.me.drive.root.get().execute_query()
        self.assertEqual(f"/me/drive/items/{result.id}", str(result.resource_path))

    def test6_resolve_drive_children_path(self):
        path = self.client.me.drive.root.children.resource_path
        assert path is not None
        item_id = uuid.uuid4().hex
        path.set_segment(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test9_resolve_site_url_path(self):
        site = self.client.sites.get_by_url(test_team_site_url).execute_query()
        self.assertEqual(f"{str(self.client.sites.resource_path)}/{site.id}", str(site.resource_path))

    def test_11_build_site_root_path(self):
        site = self.client.sites.root.get().execute_query()
        self.assertEqual(f"/sites/{site.id}", str(site.resource_path))

    def test_13_resolve_me_resource_path(self):
        current_user = self.client.me.get().execute_query()
        self.assertEqual(f"/users/{current_user.id}", str(current_user.resource_path))

    def test_15_resolve_my_drive_resource_path(self):
        my_drive = self.client.me.drive.get().execute_query()
        self.assertEqual(f"/drives/{my_drive.id}", str(my_drive.resource_path))

    def test_16_resolve_entity_type_name(self):
        name = self.client.me.joined_teams.entity_type_name
        self.assertEqual("Collection(microsoft.graph.team)", name)
