"""Offline tests for the migration-supporting site primitives.

Covers the accessors added/cleaned up for the assessment scans:
``Web.site_id``, ``Site.get_storage_metrics()``, and the ``None`` missing-value
sentinels on ``LastItem*Date`` (no more naive ``datetime.min``).
"""

from __future__ import annotations

import unittest

from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


def _ctx(payloads: list) -> ClientContext:
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = _ScriptedTransport(payloads)
    return ctx


class TestSitePrimitives(unittest.TestCase):
    def test_web_site_id(self):
        ctx = _ctx([{"d": {"__metadata": {"type": "SP.Web"}, "Id": "web-1", "SiteId": "site-1", "Url": "https://x"}}])
        web = ctx.web.get().execute_query()
        self.assertEqual(web.site_id, "site-1")
        self.assertEqual(web.id, "web-1")

    def test_site_get_storage_metrics(self):
        ctx = _ctx([{"d": {"TotalSize": 644245094400, "TotalFileCount": 120, "VersionCount": 12}}])
        metrics = ctx.site.get_storage_metrics().execute_query()
        self.assertEqual(metrics.total_size, 644245094400)  # noqa: PLR2004
        self.assertEqual(metrics.total_file_count, 120)  # noqa: PLR2004
        self.assertEqual(metrics.version_count, 12)  # noqa: PLR2004

    def test_list_last_item_modified_date_none_when_absent(self):
        ctx = _ctx(
            [
                {
                    "d": {
                        "results": [
                            {"__metadata": {"type": "SP.List"}, "Id": "1", "Title": "A", "Hidden": False},
                            {
                                "__metadata": {"type": "SP.List"},
                                "Id": "2",
                                "Title": "B",
                                "Hidden": False,
                                "LastItemModifiedDate": "2024-01-02T03:04:05Z",
                            },
                        ]
                    }
                }
            ]
        )
        lists = ctx.web.lists.get().execute_query()
        self.assertIsNone(lists[0].last_item_modified_date)
        self.assertIsNotNone(lists[1].last_item_modified_date)
        self.assertEqual(lists[1].last_item_modified_date.year, 2024)  # noqa: PLR2004

    def test_web_last_item_modified_date_none_when_absent(self):
        ctx = _ctx([{"d": {"__metadata": {"type": "SP.Web"}, "Url": "https://x"}}])
        web = ctx.web.get().execute_query()
        self.assertIsNone(web.last_item_modified_date)

    def test_ensure_folder_delegates_to_ensure_by_path(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(path)
                return "resolved-folder"

        folder._properties["Folders"] = _FakeFolders()
        self.assertEqual(folder.ensure_folder("a/b/c"), "resolved-folder")
        self.assertEqual(calls, ["a/b/c"])

    def test_ensure_folders_dedups_and_sorts(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(path)
                return "folder"

        folder._properties["Folders"] = _FakeFolders()
        result = folder.ensure_folders(["a/b", "a/b", "a/c", "docs"])
        self.assertEqual(result, folder)
        self.assertEqual(calls, ["a/b", "a/c", "docs"])  # deduped, sorted

    def test_ensure_folders_skips_ancestor_paths(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(path)
                return "folder"

        folder._properties["Folders"] = _FakeFolders()
        # "a/b" is covered by the nested "a/b/c" — only the deepest is ensured
        folder.ensure_folders(["a/b", "a/b/c", "a/b/d"])
        self.assertEqual(calls, ["a/b/c", "a/b/d"])

    def test_upload_content_dispatches_by_size(self):
        ctx = _ctx([{"d": {"results": []}}])
        files = ctx.web.root_folder.files
        files.upload_content(b"x" * 10, "small.bin")
        files.upload_content(b"x" * (4 * 1024 * 1024 + 1), "large.bin")
        self.assertTrue(ctx.has_pending_request)  # both dispatch paths built queries

    def test_folder_upload_file_ensures_parent_and_uploads(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFiles:
            def upload_content(self, content, file_name, chunk_size=4 * 1024 * 1024):
                calls.append(("upload_content", file_name))
                return "file"

        class _FakeFolder:
            @property
            def files(self):
                return _FakeFiles()

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(("ensure", path))
                return _FakeFolder()

        folder._properties["Files"] = _FakeFiles()
        folder._properties["Folders"] = _FakeFolders()

        result = folder.upload_file("a/b/c.txt", b"data")
        self.assertEqual(result, "file")
        self.assertEqual(calls, [("ensure", "a/b"), ("upload_content", "c.txt")])

        calls.clear()
        folder.upload_file("root.txt", b"data")
        self.assertEqual(calls, [("upload_content", "root.txt")])  # no parent ensure at root


if __name__ == "__main__":
    unittest.main()
