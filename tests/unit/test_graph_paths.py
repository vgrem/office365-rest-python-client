"""Offline unit tests for Graph resource-path building (no credentials required)."""

from __future__ import annotations

import unittest
import uuid

from office365.graph_client import GraphClient
from office365.onedrive.internal.paths.url import UrlPath
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath


class TestGraphPathBuilding(unittest.TestCase):
    """Building and resolving Graph resource paths is a pure in-memory operation."""

    client = GraphClient()

    def test_build_url_resource_path(self):
        path = UrlPath(
            "Sample.docx",
            ResourcePath("root", ResourcePath("drive", self.client.me.resource_path)),
        )
        self.assertEqual(str(path), "/me/drive/root:/Sample.docx:/")

    def test_build_nested_url_resource_path(self):
        parent_path = ResourcePath("root", ResourcePath("drive", self.client.me.resource_path))
        path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent_path)))
        self.assertEqual("/me/drive/root:/archive/2018/Sample.docx:/", str(path))

    def test_resolve_drive_url_path(self):
        parent_path = self.client.me.drive.root.resource_path
        assert parent_path is not None
        path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent_path)))
        item_id = uuid.uuid4().hex
        path.set_segment(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test_build_drive_children_path(self):
        item_id = uuid.uuid4().hex
        path = self.client.sites.root.drive.items[item_id].children.resource_path
        self.assertEqual(f"/sites/root/drive/items/{item_id}/children", str(path))

    def test_resolve_drive_root_path(self):
        path = self.client.me.drive.root.resource_path
        assert path is not None
        item_id = uuid.uuid4().hex
        path.set_segment(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test_resolve_term_children_path(self):
        group_id = uuid.uuid4().hex
        set_id = uuid.uuid4().hex
        term_id = uuid.uuid4().hex
        path = self.client.sites.root.term_store.groups[group_id].sets[set_id].children.resource_path
        assert path is not None
        path = path.set_segment(term_id)
        self.assertEqual(
            f"/sites/root/termStore/groups/{group_id}/sets/{set_id}/terms/{term_id}",
            str(path),
        )

    def test_build_path_from_url(self):
        path_str = "/teams('7f919b9f-c220-4290-a4d8-5ff9300d1296')/operations('dc97f61a-0040-436f-ac09-427cd2456fd8')"
        path = ODataPathBuilder.parse_url(path_str)
        self.assertIsNotNone(path.segment)
